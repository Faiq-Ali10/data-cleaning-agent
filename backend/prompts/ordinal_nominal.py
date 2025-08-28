def prompt_on(unique_values):
    return f"""I am giving you the unique values of a column.
    Please tell me if this column is ordinal or nominal:
    - Return 0 for ordinal
    - Return 1 for nominal
    Do not provide any explanation, only return 0 or 1.

    Unique values: {unique_values}
    """