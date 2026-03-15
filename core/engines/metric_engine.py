# core/engines/metric_engine.py

import numpy as np


class MetricEngine:

    def run(self, df):

        if df.empty:
            return {
                "revenue": None,
                "profit": None,
                "cost": None,
                "quantity": None
            }

        metrics = {
            "revenue": None,
            "profit": None,
            "cost": None,
            "quantity": None
        }

        for col in df.columns:

            col_lower = col.lower()

            # Skip non-numeric columns
            if not np.issubdtype(df[col].dtype, np.number):
                continue

            if any(word in col_lower for word in ["sales", "revenue", "income"]):
                if metrics["revenue"] is None:
                    metrics["revenue"] = col

            elif "profit" in col_lower:
                if metrics["profit"] is None:
                    metrics["profit"] = col

            elif any(word in col_lower for word in ["cost", "expense"]):
                if metrics["cost"] is None:
                    metrics["cost"] = col

            elif any(word in col_lower for word in ["quantity", "qty", "units"]):
                if metrics["quantity"] is None:
                    metrics["quantity"] = col

        return metrics
