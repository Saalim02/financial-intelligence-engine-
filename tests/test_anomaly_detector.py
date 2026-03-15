#tests/est_anomaly_detector.py

import pandas as pd
from core.engines.anomaly_detector import AnomalyDetector


def test_anomaly_detector_detects_outliers():

    df = pd.DataFrame({
        "revenue": [100, 110, 105, 5000]  # 5000 is outlier
    })

    engine = AnomalyDetector()
    result = engine.run(df, ["revenue"])

    assert isinstance(result, list)
    assert any("abnormal" in msg.lower() for msg in result)


def test_anomaly_detector_handles_invalid_column():

    df = pd.DataFrame({
        "revenue": [100, 200]
    })

    engine = AnomalyDetector()
    result = engine.run(df, ["non_existing"])

    assert isinstance(result, dict)
    assert "error" in result
