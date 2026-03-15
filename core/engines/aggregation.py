# core/engines/aggregation.py

import numpy as np


class AggregationEngine:

    def run(self, df, entities=None):

        if not entities:
            return {"error": "No KPI provided."}

        kpi = entities[0]

        if kpi not in df.columns:
            return {"error": f"KPI column '{kpi}' not found."}

        if not np.issubdtype(df[kpi].dtype, np.number):
            return {"error": f"KPI column '{kpi}' must be numeric."}

        identifier_columns = []

        return self._analyze_aggregations(df, kpi, identifier_columns)

    def _analyze_aggregations(self, df, kpi, identifier_columns):

        insights = []
        categorical_columns = df.select_dtypes(include="object").columns

        for col in categorical_columns:

            if col in identifier_columns:
                continue

            if df[col].nunique() <= 1:
                continue

            if df[col].nunique() > 50:
                continue

            grouped = (
                df.groupby(col)[kpi]
                .sum()
                .sort_values(ascending=False)
            )

            if grouped.empty:
                continue

            top_category = grouped.index[0]
            bottom_category = grouped.index[-1]

            insights.append(
                f"Top performing {col}: {top_category} "
                f"({round(grouped.iloc[0], 2)})"
            )

            insights.append(
                f"Lowest performing {col}: {bottom_category} "
                f"({round(grouped.iloc[-1], 2)})"
            )

        if not insights:
            return ["No aggregation insights found."]

        return insights
