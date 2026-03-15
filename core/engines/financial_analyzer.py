# core/engines/financial_analyzer.py

import numpy as np


class FinancialAnalyzer:

    def run(self, df, metrics=None):

        if df.empty:
            return {"error": "Empty dataframe."}

        if not metrics:
            return {"error": "No financial metrics provided."}

        revenue_col = metrics.get("revenue")
        profit_col = metrics.get("profit")

        insights = []

        # Validate columns
        if revenue_col and revenue_col not in df.columns:
            return {"error": f"Revenue column '{revenue_col}' not found."}

        if profit_col and profit_col not in df.columns:
            return {"error": f"Profit column '{profit_col}' not found."}

        # Ensure numeric
        if revenue_col and not np.issubdtype(df[revenue_col].dtype, np.number):
            return {"error": "Revenue column must be numeric."}

        if profit_col and not np.issubdtype(df[profit_col].dtype, np.number):
            return {"error": "Profit column must be numeric."}

        # ---------------------------------------
        # TOTAL REVENUE & PROFIT
        # ---------------------------------------
        if revenue_col:
            total_revenue = df[revenue_col].sum()
            insights.append(f"Total Revenue: {round(total_revenue, 2)}")

        if profit_col:
            total_profit = df[profit_col].sum()
            insights.append(f"Total Profit: {round(total_profit, 2)}")

            loss_rows = df[df[profit_col] < 0]
            if not loss_rows.empty:
                insights.append(
                    f"Warning: {len(loss_rows)} records show negative profit."
                )

        # ---------------------------------------
        # OVERALL MARGIN
        # ---------------------------------------
        if revenue_col and profit_col:
            total_revenue = df[revenue_col].sum()
            total_profit = df[profit_col].sum()

            if total_revenue != 0:
                overall_margin = total_profit / total_revenue
                insights.append(
                    f"Overall Profit Margin: {round(overall_margin * 100, 2)}%"
                )

        # ---------------------------------------
        # REGION-WISE FINANCIAL ANALYSIS
        # ---------------------------------------
        region_col = None
        for col in df.columns:
            if "region" in col.lower():
                region_col = col
                break

        if revenue_col and profit_col and region_col:

            region_group = (
                df.groupby(region_col)[[revenue_col, profit_col]]
                .sum()
            )

            # Avoid division by zero
            region_group["Margin"] = np.where(
                region_group[revenue_col] != 0,
                region_group[profit_col] / region_group[revenue_col],
                0
            )

            if not region_group.empty:

                top_profit_region = region_group[profit_col].idxmax()
                worst_profit_region = region_group[profit_col].idxmin()

                insights.append(
                    f"Most Profitable Region: {top_profit_region} "
                    f"({round(region_group.loc[top_profit_region, profit_col], 2)})"
                )

                insights.append(
                    f"Worst Performing Region (Profit): {worst_profit_region} "
                    f"({round(region_group.loc[worst_profit_region, profit_col], 2)})"
                )

                highest_margin_region = region_group["Margin"].idxmax()
                lowest_margin_region = region_group["Margin"].idxmin()

                insights.append(
                    f"Highest Margin Region: {highest_margin_region} "
                    f"({round(region_group.loc[highest_margin_region, 'Margin'] * 100, 2)}%)"
                )

                insights.append(
                    f"Lowest Margin Region: {lowest_margin_region} "
                    f"({round(region_group.loc[lowest_margin_region, 'Margin'] * 100, 2)}%)"
                )

                loss_regions = region_group[region_group[profit_col] < 0]

                if not loss_regions.empty:
                    loss_list = ", ".join(loss_regions.index.tolist())
                    insights.append(f"Loss-Making Regions: {loss_list}")

        if not insights:
            return ["No financial insights generated."]

        return insights
