# core/engines/insights.py

import numpy as np


class InsightGenerator:

    def run(self, df, profile):

        if df.empty:
            return {"error": "Empty dataframe."}

        if not profile:
            return {"error": "Profile data missing."}

        insights = []

        missing_values = profile.get("missing_values", {})
        numeric_columns = profile.get("numeric_columns", [])
        duplicate_rows = profile.get("duplicate_rows", 0)

        # -------------------------
        # Missing values
        # -------------------------
        for col, count in missing_values.items():
            if count > 0:
                insights.append(
                    f"Column '{col}' has {count} missing values."
                )

        # -------------------------
        # High variance
        # -------------------------
        for col in numeric_columns:
            if col not in df.columns:
                continue

            series = df[col].dropna()

            if series.empty:
                continue

            mean_val = series.mean()
            std_val = series.std()

            if mean_val != 0 and std_val > abs(mean_val):
                insights.append(
                    f"Column '{col}' shows high variability."
                )

        # -------------------------
        # Skewness
        # -------------------------
        for col in numeric_columns:
            if col not in df.columns:
                continue

            series = df[col].dropna()

            if series.empty:
                continue

            skewness = series.skew()

            if abs(skewness) > 1:
                insights.append(
                    f"Column '{col}' is highly skewed."
                )

        # -------------------------
        # Duplicate rows
        # -------------------------
        if duplicate_rows > 0:
            insights.append(
                f"Dataset contains {duplicate_rows} duplicate rows."
            )

        if not insights:
            return ["Dataset appears clean with no major issues detected."]

        return insights
