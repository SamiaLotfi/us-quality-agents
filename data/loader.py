import pandas as pd

def load_stories_from_excel(file_path: str) -> list[str]:
    """
    Load and format user stories from an Excel file using 'title' and 'description'.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        List of user stories as strings.
    """
    df = pd.read_excel(file_path)

    required_cols = {"title", "description"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Excel must contain columns: {required_cols}")

    # Combine title + description
    stories = (df["title"].fillna("") + ". " + df["description"].fillna("")).str.strip().tolist()
    return stories
