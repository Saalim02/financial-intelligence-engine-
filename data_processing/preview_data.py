#data_preprocessing/preview_data.py
import pandas as pd
import os


def preview_csv(file_path: str, rows: int = 5) -> dict:
    """
    Return first few rows of the CSV file.
    """

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    if not isinstance(rows, int) or rows <= 0:
        return {
            "status": "error",
            "message": "Rows parameter must be a positive integer."
        }

    try:
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="latin-1")

        if df.empty:
            return {
                "status": "error",
                "message": "CSV file is empty."
            }

        preview_data = df.head(rows).to_dict(orient="records")

        return {
            "status": "success",
            "rows_returned": len(preview_data),
            "preview": preview_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
