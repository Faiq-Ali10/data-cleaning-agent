def prompt_mapping(unique_values):
    return f"""
Given these unique values from a column that is ordinal, create a Python dictionary mapping them to integers 
starting at 1 in ascending order, preserving their natural order.

Unique values: {unique_values}

Output ONLY the Python dictionary, nothing else.
"""