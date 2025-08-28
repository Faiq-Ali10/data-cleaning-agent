import pandas as pd
from backend.llm import LLM
import ast
import json
import re
from io import StringIO
from backend.prompts.ordinal_mapping import prompt_mapping
from backend.prompts.ordinal_nominal import prompt_on
from backend.prompts.column_types import prompt_column_types
from backend.prompts.preprocssing_prompt import prompt_preprocess     

class DataClean:
    def __init__(self) -> None:
        self.llm = LLM().get_llm()
        self.max_category = 50
        self.scheme = None
        
    def clean_llm_csv(self, answer: str) -> str:
        lines = answer.strip().splitlines()
        # remove leading "csv" or markdown formatting
        if lines[0].lower().strip() in ["csv", "```csv", "```"]:
            lines = lines[1:]
        if lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines)  
        
    def dataframe_datatypes(self, df):
        prompt = prompt_column_types(df)
        answer_json = self.llm.invoke(prompt)
        print("@@llm@@")
        print(answer_json)
        answer_json = re.search(r"\{.*\}", answer_json, re.DOTALL)
        print("@@regex@@")
        print(answer_json)
        if answer_json:
            answer_json = answer_json.group(0)
            print("real")
            print(answer_json)
        
        try:
            answer = None
            if answer_json is not None:
                answer = json.loads(answer_json)
                
            print("@@aswer@@")
            print(answer)
            return answer
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM output is not valid JSON: {e}")
        
    def fill_na(self, df):
        self.scheme = self.dataframe_datatypes(df)
        if self.scheme is not None:
            for col in list(df.columns):
                if pd.api.types.is_datetime64_any_dtype(df[col]) and self.scheme[col] == "datetime":
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    continue
                
                if pd.api.types.is_complex_dtype(df[col]) and self.scheme[col] == "complex_number":
                    df[col] = df[col].fillna(0+0j)
                    continue
                
                try:
                    if self.scheme[col] == "int":
                        df[col] = pd.to_numeric(df[col], errors='raise').astype("Int64")
                    elif self.scheme[col] == "float":
                        df[col] = pd.to_numeric(df[col], errors='raise')
                except Exception:
                    pass  
                
                nunique = df[col].nunique()
                if pd.api.types.is_numeric_dtype(df[col]) \
                    and not pd.api.types.is_timedelta64_dtype(df[col]) \
                    and not pd.api.types.is_complex_dtype(df[col]) \
                    and not pd.api.types.is_bool_dtype(df[col]):
                    skewness = df[col].skew()
                    
                    if isinstance(skewness, (int, float)) and abs(skewness) > 0.5:
                        df[col] = df[col].fillna(df[col].median())  
                    else:
                        if nunique > 10:
                            df[col] = df[col].fillna(df[col].mean()) 
                        else:
                            df[col] = df[col].fillna(df[col].mode()[0])    
                else:
                    if self.scheme[col] == "string":
                        df[col] = df[col].fillna("unknown")  
               
        print("@@ Before sending to LLM @@")
        print(df)
        return df
    
    def llm_handling(self, df, batch_size):
        print("@@llm handling@@")
        if df is None or df.empty:
            return df  # nothing to process
    
        data = []
        for i in range(0, len(df), batch_size):
            answer = self.llm.invoke(prompt_preprocess(df.iloc[i : i + batch_size]))
            clean = self.clean_llm_csv(answer)
            data.append(pd.read_csv(StringIO(clean)))
            
        processed = pd.concat(data, ignore_index=False)
        print("@@ After LLM @@")
        print(processed)
        return processed
                        
    def encoding(self, df):
        if self.scheme is not None:
            for col, dtype in self.scheme.items():
                if col not in df.columns:
                    continue
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    if str(dtype) in ["int", "float", "complex_number"]:
                        df[col] = pd.to_numeric(df[col], errors = "coerce")
                    elif "datetime" in str(dtype):
                        df[col] = pd.to_datetime(df[col], errors = "coerce")
            
        for col in list(df.columns):
            if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]): # type: ignore
                nunique = df[col].nunique()
                if nunique / len(df[col]) < 0.05:
                    nominal = self.llm.invoke(prompt_on(df[col].unique()))
                    if int(nominal):
                        if nunique <= self.max_category:
                            df = pd.get_dummies(df, columns=[col], drop_first=True)
                        else:
                            freq_map = df[col].value_counts(normalize=True) 
                            df[col] = df[col].map(freq_map)
                    else:
                        ordinal_mapping = ast.literal_eval(self.llm.invoke(prompt_mapping(df[col].unique())))
                        df[col] = df[col].map(ordinal_mapping)
           
        print("@@ Final after encoding @@")
        print(df)            
        return df