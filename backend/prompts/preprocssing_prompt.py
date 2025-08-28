def prompt_preprocess(rows):
    return f"""
    You are a data cleaning assistant specializing in normalizing categorical string values.

    You will receive a small table (≤20 rows) from a larger dataset. 
    Your goal is to:
    - Detect when multiple different strings represent the same category (e.g., "NY", "ny", "New York" → "New York").
    - Fix typos and spelling variations while keeping meaning intact.
    - Remove leading/trailing spaces and standardize capitalization:
        - Proper nouns → Title Case ("New York").
        - Acronyms → Uppercase ("USA").
    - For numeric columns:
        - Convert number words (e.g., "thirty") into digits (30).
        - Preserve valid numeric values.
    - Replace placeholders for missing values (e.g., "not available", "missing", "N/A", "none", "null") with NaN.
    - Do not merge unrelated categories.
    - Keep table shape identical — same number of rows and columns.
    - Return the cleaned table in valid CSV format with headers.

    Do not perform encoding — just standardize text values.

    Table:
    {rows}
    """