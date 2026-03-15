import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Engines
from core.engines.aggregation import AggregationEngine
from core.engines.time_analyzer import TimeAnalyzer
from core.engines.anomaly_detector import AnomalyDetector
from core.engines.correlation import CorrelationEngine
from core.engines.financial_analyzer import FinancialAnalyzer
from core.engines.metric_engine import MetricEngine
from core.engines.sql_engine import SQLEngine

# Agent
from core.agent.financial_agent import FinancialAgent

# Utils
from utils.chart_generator import generate_chart


# -------------------------------------
# PAGE CONFIG
# -------------------------------------

st.set_page_config(
    page_title="Autonomous Financial Intelligence Engine",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Autonomous Financial Intelligence Engine")

st.markdown(
"""
**PowerBI + ChatGPT + Autonomous Analyst**

Upload dataset → Explore dashboard → Chat with AI analyst
"""
)

# -------------------------------------
# SIDEBAR
# -------------------------------------

st.sidebar.header("⚙ Configuration")

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

mode = st.sidebar.selectbox(
    "Answer Mode",
    ["Insight", "SQL", "Dashboard"]
)

if not api_key:
    st.warning("Enter OpenAI API key")
    st.stop()

if not uploaded_file:
    st.info("Upload dataset to start")
    st.stop()


# -------------------------------------
# LOAD DATA
# -------------------------------------

if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -------------------------------------
# INITIALIZE ENGINES
# -------------------------------------

engines = {
    "aggregation": AggregationEngine(),
    "time": TimeAnalyzer(),
    "anomaly": AnomalyDetector(),
    "correlation": CorrelationEngine(),
    "financial": FinancialAnalyzer(),
    "metric": MetricEngine(),
    "sql": SQLEngine()
}

agent = FinancialAgent(
    engines=engines,
    api_key=api_key
)

# -------------------------------------
# DATASET OVERVIEW
# -------------------------------------

st.header("📊 Dataset Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Rows", df.shape[0])
c2.metric("Columns", df.shape[1])
c3.metric("Missing Values", int(df.isna().sum().sum()))
c4.metric("Duplicate Rows", int(df.duplicated().sum()))

st.dataframe(df.head())

# -------------------------------------
# KPI SUMMARY
# -------------------------------------

st.subheader("📈 Key Financial Statistics")

numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:

    k1, k2, k3 = st.columns(3)

    k1.metric("Average Value", round(numeric_df.mean().mean(), 2))
    k2.metric("Maximum Value", round(numeric_df.max().max(), 2))
    k3.metric("Minimum Value", round(numeric_df.min().min(), 2))

# -------------------------------------
# TREND VISUALIZATION
# -------------------------------------

st.subheader("📉 Trend Visualization")

numeric_cols = numeric_df.columns.tolist()

if numeric_cols:

    selected_column = st.selectbox(
        "Select metric for trend",
        numeric_cols
    )

    fig = px.line(df, y=selected_column)

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------
# CORRELATION HEATMAP
# -------------------------------------

st.subheader("📊 Correlation Heatmap")

if len(numeric_cols) >= 2:

    corr = df.corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.heatmap(corr, cmap="coolwarm", annot=True, ax=ax)

    st.pyplot(fig)

# -------------------------------------
# ANOMALY DETECTION
# -------------------------------------

st.subheader("⚠️ Anomaly Detection")

selected_metrics = st.multiselect(
    "Select metrics",
    numeric_cols
)

if selected_metrics:

    anomalies = engines["anomaly"].run(df, selected_metrics)

    st.write(anomalies)

# -------------------------------------
# AGGREGATION INSIGHTS
# -------------------------------------

st.subheader("📊 Aggregation Insights")

agg_col = st.selectbox(
    "Select KPI column",
    numeric_cols
)

if st.button("Generate Aggregation Insights"):

    insights = engines["aggregation"].run(df, [agg_col])

    for insight in insights:
        st.info(insight)

# -------------------------------------
# AUTONOMOUS ANALYST
# -------------------------------------

st.header("🤖 Autonomous Data Analyst")

if st.button("Generate AI Insights"):

    auto_insights = []

    auto_insights += engines["aggregation"].run(df, [agg_col])
    auto_insights += engines["anomaly"].run(df, numeric_cols[:2])

    for insight in auto_insights:
        st.write(insight)

# -------------------------------------
# AI CHAT ANALYST
# -------------------------------------

st.header("💬 AI Financial Analyst")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input("Ask questions about your dataset")

if user_prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.write(user_prompt)

    with st.spinner("AI analyzing dataset..."):

        response = agent.ask(
            user_prompt,
            df,
            mode=mode
        )

    # -------------------------------------
    # HANDLE ERROR
    # -------------------------------------

    if isinstance(response, dict) and "error" in response:

        with st.chat_message("assistant"):
            st.error(response["error"])

        st.stop()

    answer = response.get("final_answer", [])

    st.session_state.messages.append({
        "role": "assistant",
        "content": str(answer)
    })

    # -------------------------------------
    # DISPLAY RESPONSE
    # -------------------------------------

    with st.chat_message("assistant"):

        # ---------------- SQL MODE ----------------

        if mode == "SQL":

            st.subheader("Generated SQL Query")

            st.code(response.get("sql_query", ""), language="sql")

            if isinstance(answer, list) and len(answer) > 0:
                st.dataframe(pd.DataFrame(answer))
            else:
                st.info("No results returned.")

        # ---------------- DASHBOARD MODE ----------------

        elif mode == "Dashboard":

            if isinstance(answer, list) and len(answer) > 0:

                df_result = pd.DataFrame(answer)

                st.dataframe(df_result)

                chart = generate_chart(answer)

                if chart:
                    st.plotly_chart(chart, use_container_width=True)

            else:
                st.info("No dashboard data available.")

        # ---------------- INSIGHT MODE ----------------

        else:

            if "insight" in response:
                st.info(response["insight"])

            if isinstance(answer, list) and len(answer) > 0:

                df_result = pd.DataFrame(answer)

                st.dataframe(df_result)

                chart = generate_chart(answer)

                if chart:
                    st.plotly_chart(chart, use_container_width=True)

            else:
                st.write(answer)