#data_preprocessing/describe_data.py

import pandas as pd
import os


def describe_csv(file_path: str) -> dict:
    """
    Return statistical summary of the CSV file.
    """

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    try:
        df = pd.read_csv(file_path)

        if df.empty:
            return {
                "status": "error",
                "message": "CSV file is empty."
            }

        numeric_summary = df.describe().to_dict()
        categorical_summary = (
            df.describe(include="object").to_dict()
            if not df.select_dtypes(include="object").empty
            else {}
        )

        return {
            "status": "success",
            "numeric_summary": numeric_summary,
            "categorical_summary": categorical_summary,
            "rows": df.shape[0],
            "columns": df.shape[1]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
