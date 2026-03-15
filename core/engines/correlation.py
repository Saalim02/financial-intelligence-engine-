# core/engines/correlation.py

import numpy as np


class CorrelationEngine:

    def run(self, df, entities=None):

        if df.empty:
            return {"error": "Empty dataframe."}

        numeric_df = df.select_dtypes(include=np.number)

        if numeric_df.shape[1] < 2:
            return {"error": "Not enough numeric columns for correlation analysis."}

        corr_matrix = numeric_df.corr().dropna(how="all").fillna(0)

        strongest_pair = None
        strongest_value = 0

        columns = corr_matrix.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                col1 = columns[i]
                col2 = columns[j]

                value = abs(corr_matrix.iloc[i, j])

                if value > 0.3 and value > strongest_value:
                    strongest_value = value
                    strongest_pair = (col1, col2)

        if strongest_pair:
            return {
                "strongest_pair": strongest_pair,
                "correlation": round(strongest_value, 3)
            }

        return ["No strong correlations detected (>|0.3|)."]
