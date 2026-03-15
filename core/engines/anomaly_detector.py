# core/engines/anomaly_detector.py

import numpy as np


class AnomalyDetector:

    def run(self, df, entities=None):

        if df.empty:
            return {"error": "Empty dataframe."}

        if not entities:
            return {"error": "No metric provided for anomaly detection."}

        insights = []
        valid_metric_found = False

        for column in entities:

            if column not in df.columns:
                continue

            if not np.issubdtype(df[column].dtype, np.number):
                continue

            series = df[column].dropna()

            if series.empty:
                continue

            valid_metric_found = True

            outliers = self._iqr_outliers(series)

            if not outliers.empty:
                insights.append(
                    f"{len(outliers)} abnormal records detected in '{column}' (IQR method)."
                )

            extreme_low = series[series < series.quantile(0.01)]

            if not extreme_low.empty:
                insights.append(
                    f"{len(extreme_low)} extreme low values in '{column}' (bottom 1%)."
                )

        if not valid_metric_found:
            return {"error": "No valid numeric metric found for anomaly detection."}

        if not insights:
            return ["No anomalies detected."]

        return insights

    def _iqr_outliers(self, series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return series[(series < lower) | (series > upper)]
