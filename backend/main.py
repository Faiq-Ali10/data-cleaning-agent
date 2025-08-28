from fastapi import FastAPI, File, UploadFile, Response
from backend.agent import Agent, AgentState
import os
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO
from typing import cast
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
os.environ["GOOGLE_API_KEY"] = str(os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/preprocess")
async def preprocess(file : UploadFile = File(...)):
    if not file.filename:  # handle None
        return {"error": "No filename provided"}
    
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    
    df = None
    try:
        contents = await file.read()
        if ext == ".csv":
            df = pd.read_csv(BytesIO(contents), on_bad_lines="skip")
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(BytesIO(contents))
        else:
            return {"message" : "Please upload csv or excel"}
    except Exception as e:
        print(f"error : {repr(e)}")
        
    if df is None or df.empty:
        return {"error": "File read failed or contains no data"}
    
    agent = Agent(df)
    app = agent.get_app()
    query = cast(AgentState, {"input" : df})
    
    processed_df = None
    try:
        processed_df = app.invoke(query).get("output")
        if not isinstance(processed_df, pd.DataFrame):
            return {"message" : "fail processing failed"}
    except Exception as e:
        print(f"error : {repr(e)}")
    
    if not isinstance(processed_df, pd.DataFrame):
        return {"error": "Agent did not return a valid DataFrame123"}
    
    return Response(
    processed_df.to_csv(index=False),
    media_type="text/csv",
    headers={"Content-Disposition": "attachment; filename=processed.csv"}
)