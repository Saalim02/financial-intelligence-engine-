import pandas as pd
import plotly.express as px


def generate_chart(data):
    """
    Automatically generate the best chart for SQL results.
    """

    if not isinstance(data, list) or len(data) == 0:
        return None

    df = pd.DataFrame(data)

    if df.empty:
        return None

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    non_numeric_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

    # ------------------------------------
    # Case 1: Category vs Numeric → Bar Chart
    # ------------------------------------

    if len(non_numeric_cols) >= 1 and len(numeric_cols) >= 1:

        x_col = non_numeric_cols[0]
        y_col = numeric_cols[0]

        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=f"{y_col} by {x_col}"
        )

        return fig

    # ------------------------------------
    # Case 2: Time Series → Line Chart
    # ------------------------------------

    for col in df.columns:

        if "date" in col or "year" in col or "month" in col:

            if len(numeric_cols) >= 1:

                fig = px.line(
                    df,
                    x=col,
                    y=numeric_cols[0],
                    title=f"{numeric_cols[0]} Trend"
                )

                return fig

    # ------------------------------------
    # Case 3: Two Numeric Columns → Scatter
    # ------------------------------------

    if len(numeric_cols) >= 2:

        fig = px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
        )

        return fig

    return None