# core/engines/eda_engine.py

class EDAEngine:

    def __init__(
        self,
        profiler,
        kpi_detector,
        metric_engine,
        financial_engine,
        time_engine,
        anomaly_engine,
        correlation_engine,
        aggregation_engine,
        insight_generator,
        insight_ranker
    ):
        self.profiler = profiler
        self.kpi_detector = kpi_detector
        self.metric_engine = metric_engine
        self.financial_engine = financial_engine
        self.time_engine = time_engine
        self.anomaly_engine = anomaly_engine
        self.correlation_engine = correlation_engine
        self.aggregation_engine = aggregation_engine
        self.insight_generator = insight_generator
        self.insight_ranker = insight_ranker

    def run(self, df):

        profile = self.profiler.run(df)

        kpi = self.kpi_detector.run(df)

        metrics = self.metric_engine.run(df)

        metric_columns = [
            col for col in metrics.values()
            if col is not None
        ]

        financial_insights = self.financial_engine.run(df, metrics)

        time_insights = self.time_engine.run(
            df,
            [kpi] if kpi else None
        )

        anomaly_insights = self.anomaly_engine.run(
            df,
            metric_columns if metric_columns else None
        )

        correlation = self.correlation_engine.run(df)

        aggregation_insights = self.aggregation_engine.run(
            df,
            [kpi] if kpi else None
        )

        general_insights = self.insight_generator.run(df, profile)

        ranked = self.insight_ranker.run({
            "financial": financial_insights,
            "time": time_insights,
            "anomaly": anomaly_insights,
            "general": general_insights
        })

        return {
            "profile": profile,
            "kpi": kpi,
            "metrics": metrics,
            "financial_insights": financial_insights,
            "time_insights": time_insights,
            "anomaly_insights": anomaly_insights,
            "correlation": correlation,
            "aggregation_insights": aggregation_insights,
            "general_insights": general_insights,
            "ranked_insights": ranked
        }
