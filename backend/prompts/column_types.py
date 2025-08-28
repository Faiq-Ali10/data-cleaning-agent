def prompt_column_types(df):
    formatted = []
    for col in df.columns:
        rows = "\n".join([str(val) for val in df[col].head().tolist()])
        formatted.append(f"Column: {col}\nSample values:\n{rows}")

    return f"""
    You are a data schema assistant.
    You will be shown dataset column names with a few sample values.

    Task: Infer the most appropriate *intended* datatype for each column, 
    not just from the samples but also from the column name semantics.

    Allowed types:
    - "int"
    - "float"
    - "complex_number"
    - "boolean"
    - "string"
    - "datetime"

    Rules:
    - Respond with valid JSON only.
    - Do not include explanations, code fences, or markdown.
    - Treat placeholders like "NaN", "not available", "missing", "N/A", "none", "null", or empty strings as missing values, not strings.
    - Prefer "int" for IDs and whole number counts (e.g., Age, EmployeeID).
    - Prefer "float" for monetary amounts or values that may contain decimals (e.g., Salary).
    - Prefer "datetime" if values look like dates.
    - Use "string" only if the data is textual by nature (e.g., Name, Email, Department).

    Output format:
    {{
      "ColumnA": "int",
      "ColumnB": "string"
    }}

    Dataset:
    {chr(10).join(formatted)}

    Now respond with JSON only:
    """
