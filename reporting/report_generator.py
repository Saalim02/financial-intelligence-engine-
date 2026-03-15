#reporting/report_generator.py
def generate_report(eda_output):

    if not eda_output:
        return "No data available to generate report."

    profile = eda_output.get("profile", {})
    insights = eda_output.get("general_insights", [])
    kpi = eda_output.get("kpi")
    correlation = eda_output.get("correlation")
    aggregation = eda_output.get("aggregation_insights")
    metrics = eda_output.get("metrics")
    financial_insights = eda_output.get("financial_insights")
    time_insights = eda_output.get("time_insights")
    anomalies = eda_output.get("anomaly_insights")
    ranked = eda_output.get("ranked_insights")

    report = f"""
DATASET SUMMARY REPORT
-----------------------
Shape: {profile.get('shape')}
Columns: {profile.get('columns')}

Numeric Columns: {profile.get('numeric_columns')}
Categorical Columns: {profile.get('categorical_columns')}

Primary KPI Detected: {kpi}

Duplicate Rows: {profile.get('duplicate_rows')}
"""

    # -----------------------------
    # FINANCIAL METRICS
    # -----------------------------
    if metrics:
        report += "\n\nDETECTED FINANCIAL METRICS:\n"
        for key, value in metrics.items():
            if value:
                report += f"\n- {key.capitalize()}: {value}"

    # -----------------------------
    # FINANCIAL HEALTH
    # -----------------------------
    if isinstance(financial_insights, list):
        report += "\n\nFINANCIAL HEALTH ANALYSIS:\n"
        for item in financial_insights:
            report += f"\n- {item}"

    # -----------------------------
    # TIME TRENDS
    # -----------------------------
    if isinstance(time_insights, list):
        report += "\n\nTIME-BASED FINANCIAL TRENDS:\n"
        for item in time_insights:
            report += f"\n- {item}"

    # -----------------------------
    # CORRELATION
    # -----------------------------
    if isinstance(correlation, dict) and "strongest_pair" in correlation:
        report += (
            f"\n\nStrongest Correlation: "
            f"{correlation['strongest_pair']} → {correlation['correlation']}"
        )

    # -----------------------------
    # AGGREGATION
    # -----------------------------
    if isinstance(aggregation, list):
        report += "\n\nAGGREGATION INSIGHTS:\n"
        for item in aggregation:
            report += f"\n- {item}"

    # -----------------------------
    # GENERAL INSIGHTS
    # -----------------------------
    if isinstance(insights, list):
        report += "\n\nGENERAL INSIGHTS:\n"
        for insight in insights:
            report += f"\n- {insight}"

    # -----------------------------
    # ANOMALIES
    # -----------------------------
    if isinstance(anomalies, list):
        report += "\n\nSTATISTICAL ANOMALIES DETECTED:\n"
        for item in anomalies:
            report += f"\n- {item}"

    # -----------------------------
    # PRIORITIZED INSIGHTS
    # -----------------------------
    if isinstance(ranked, list):
        report += "\n\nPRIORITIZED INSIGHTS:\n"
        for item in ranked:
            if isinstance(item, dict):
                report += f"\n[{item.get('level')}] {item.get('message')}"
            else:
                report += f"\n{item}"

    return report.strip()
