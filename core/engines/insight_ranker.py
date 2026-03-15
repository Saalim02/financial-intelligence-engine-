# core/engines/insight_ranker.py

class InsightRanker:

    def run(self, eda_output):

        if not eda_output:
            return {"error": "No insights provided for ranking."}

        ranked = []

        financial = eda_output.get("financial", [])
        time_trends = eda_output.get("time", [])
        general = eda_output.get("general", [])
        anomalies = eda_output.get("anomaly", [])

        # Combine critical categories
        combined = financial + time_trends + anomalies

        for item in combined:

            if not isinstance(item, str):
                continue

            text = item.lower()

            level = "INFO"

            if "negative profit" in text:
                level = "CRITICAL"

            elif "extreme loss" in text:
                level = "CRITICAL"

            elif "growth" in text and "-" in text:
                level = "CRITICAL"

            elif "abnormal" in text:
                level = "WARNING"

            elif "lowest margin" in text:
                level = "WARNING"

            ranked.append({
                "level": level,
                "message": item
            })

        # General insights
        for item in general:

            if not isinstance(item, str):
                continue

            text = item.lower()

            level = "INFO"

            if "missing" in text:
                level = "WARNING"

            elif "skewed" in text:
                level = "WARNING"

            ranked.append({
                "level": level,
                "message": item
            })

        if not ranked:
            return ["No insights available for ranking."]

        return ranked
