# core/engines/profiler.py

import pandas as pd
import numpy as np


class Profiler:

    def run(self, df: pd.DataFrame):

        if df.empty:
            return {
                "shape": df.shape,
                "columns": [],
                "numeric_columns": [],
                "categorical_columns": [],
                "identifier_columns": [],
                "missing_values": {},
                "duplicate_rows": 0,
                "basic_statistics": {}
            }

        identifier_columns = self._detect_identifier_columns(df)

        numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

        # Remove identifier-like numeric columns
        numeric_columns = [
            col for col in numeric_columns
            if col not in identifier_columns
        ]

        profile = {
            "shape": df.shape,
            "columns": list(df.columns),
            "numeric_columns": numeric_columns,
            "categorical_columns": list(df.select_dtypes(include="object").columns),
            "identifier_columns": identifier_columns,
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "basic_statistics": self._safe_describe(df)
        }

        return profile

    def _detect_identifier_columns(self, df):

        identifier_cols = []

        for col in df.columns:

            col_lower = col.lower()

            # Rule 1: name-based detection
            if any(keyword in col_lower for keyword in ["id", "code", "number", "no"]):
                identifier_cols.append(col)
                continue

            # Rule 2: high uniqueness ratio
            if len(df) > 0:
                unique_ratio = df[col].nunique(dropna=True) / len(df)

                if unique_ratio > 0.95:
                    identifier_cols.append(col)

        return identifier_cols

    def _safe_describe(self, df):

        try:
            return df.describe(include="all").to_dict()
        except Exception:
            return {}
