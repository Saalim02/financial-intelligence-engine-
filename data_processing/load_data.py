#data_preprocessing/load_data.py
import pandas as pd
import os


def load_csv(file_path: str) -> dict:
    """
    Load a CSV file and return basic metadata.
    """

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
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

        return {
            "status": "success",
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": list(df.columns)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
