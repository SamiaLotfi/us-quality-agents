import pandas as pd

def save_evaluator_results(results: list[dict], output_path: str):
    """
    Save evaluator-only results to Excel.

    Args:
        results (list of dict): Each dict contains original story, scores, explanations, and flags.
        output_path (str): Path to save the Excel file.
    """
    records = []

    for r in results:
        row = {
            "original": r.get("original", ""),
            "needs_review": r.get("needs_review", False)
        }

        if "scores" in r:
            row.update({f"{k}_score": v for k, v in r["scores"].items()})
        if "explanations" in r:
            row.update({f"{k}_explanation": v for k, v in r["explanations"].items()})

        records.append(row)

    df = pd.DataFrame(records)
    df.to_excel(output_path, index=False)
