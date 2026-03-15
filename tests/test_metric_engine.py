#tests/test_metric_engine.py
import pandas as pd
from core.engines.metric_engine import MetricEngine


def test_metric_engine_detects_columns():

    df = pd.DataFrame({
        "product": ["A", "B"],
        "sales": [1000, 2000],
        "profit": [200, 500],
        "cost": [400, 800],
        "quantity": [10, 20]
    })

    engine = MetricEngine()
    result = engine.run(df)

    assert result["revenue"] == "sales"
    assert result["profit"] == "profit"
    assert result["cost"] == "cost"
    assert result["quantity"] == "quantity"


def test_metric_engine_handles_no_numeric_columns():

    df = pd.DataFrame({
        "product": ["A", "B"]
    })

    engine = MetricEngine()
    result = engine.run(df)

    assert result["revenue"] is None
    assert result["profit"] is None
