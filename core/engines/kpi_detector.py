# core/engines/kpi_detector.py

import numpy as np


class KPIDetector:

    def run(self, df):

        if df.empty:
            return None

        # -------------------------
        # Keyword-based detection
        # -------------------------
        for col in df.columns:
            col_lower = col.lower()

            if any(word in col_lower for word in ["sales", "revenue", "income"]):
                if np.issubdtype(df[col].dtype, np.number):
                    return col

        # -------------------------
        # Fallback: highest variance numeric column
        # -------------------------
        numeric_columns = df.select_dtypes(include=np.number).columns

        if len(numeric_columns) > 0:

            variances = (
                df[numeric_columns]
                .var()
                .dropna()
                .sort_values(ascending=False)
            )

            if not variances.empty:
                return variances.index[0]

        return None
