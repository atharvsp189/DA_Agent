def query_dataframe(df, code: str):
    """Executes Python code on the dataframe `df` and returns result + code."""
    try:
        # Eval the result
        print("Generated Code: ", code)
        result = eval(code)
        return result
    except Exception as e:
        return f"Error: {e}"
