import streamlit as st


def show_auto_insights(eda_engine, df):

    st.subheader("Autonomous AI Insights")

    if st.button("Generate Insights"):

        result = eda_engine.run(df)

        insights = result.get("ranked_insights", [])

        if not insights:
            st.info("No insights detected")
            return

        for item in insights:

            level = item.get("level", "INFO")
            msg = item.get("message", "")

            if level == "CRITICAL":
                st.error(msg)

            elif level == "WARNING":
                st.warning(msg)

            else:
                st.info(msg)