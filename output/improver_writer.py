import pandas as pd

def save_improver_results(results: list[dict], output_path: str):
    """
    Save improver-only results to Excel.

    Args:
        results (list of dict): Each dict contains original, improved, and justification.
        output_path (str): Path to save the Excel file.
    """
    records = []

    for r in results:
        row = {
            "original": r.get("original", ""),
            "improved": r.get("improved", ""),
            "justification": r.get("justification", "")
        }
        records.append(row)

    df = pd.DataFrame(records)
    df.to_excel(output_path, index=False)
