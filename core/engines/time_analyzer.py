# core/engines/time_analyzer.py

import pandas as pd
import numpy as np


class TimeAnalyzer:

    def run(self, df, entities=None):

        if df.empty:
            return {"error": "Empty dataframe."}

        # Identify metric column from entities
        metric_col = None
        if entities:
            for col in entities:
                if col in df.columns and np.issubdtype(df[col].dtype, np.number):
                    metric_col = col
                    break

        if not metric_col:
            return {"error": "No numeric metric provided for trend analysis."}

        # Detect date column automatically
        date_column = self._detect_date_column(df)

        if not date_column:
            return {"error": "No date column detected."}

        temp_df = df.copy()

        temp_df[date_column] = pd.to_datetime(temp_df[date_column], errors="coerce")

        if temp_df[date_column].isnull().all():
            return {"error": "Date column could not be parsed."}

        temp_df["Year"] = temp_df[date_column].dt.year

        yearly_group = temp_df.groupby("Year")[metric_col].sum()

        if yearly_group.empty:
            return {"error": "Insufficient data for trend analysis."}

        insights = []

        # Best and worst year
        best_year = yearly_group.idxmax()
        worst_year = yearly_group.idxmin()

        insights.append(
            f"Best {metric_col} Year: {best_year} "
            f"({round(yearly_group.loc[best_year], 2)})"
        )

        insights.append(
            f"Worst {metric_col} Year: {worst_year} "
            f"({round(yearly_group.loc[worst_year], 2)})"
        )

        # Growth calculation
        if len(yearly_group) > 1:
            first_year = yearly_group.index.min()
            last_year = yearly_group.index.max()

            first_value = yearly_group.loc[first_year]
            last_value = yearly_group.loc[last_year]

            if first_value != 0:
                growth = (last_value - first_value) / first_value * 100
                insights.append(
                    f"{metric_col} Growth from {first_year} to {last_year}: "
                    f"{round(growth, 2)}%"
                )

        return insights

    def _detect_date_column(self, df):
        for col in df.columns:
            if "date" in col.lower():
                return col
        return None
