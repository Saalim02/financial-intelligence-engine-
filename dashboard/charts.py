import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def show_trend_chart(df):

    date_col = None

    for col in df.columns:
        if "date" in col.lower():
            date_col = col

    if not date_col:
        return

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    trend = df.groupby(df[date_col].dt.year).size()

    st.subheader("Orders Trend")

    st.line_chart(trend)


def show_correlation(df):

    numeric = df.select_dtypes(include="number")

    if numeric.shape[1] < 2:
        return

    corr = numeric.corr()

    fig, ax = plt.subplots()

    sns.heatmap(corr, cmap="coolwarm", ax=ax)

    st.subheader("Correlation Heatmap")

    st.pyplot(fig)