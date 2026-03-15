#tests/test_time_analyzer
import pandas as pd
from core.engines.time_analyzer import TimeAnalyzer


def test_time_analyzer_detects_trend():

    df = pd.DataFrame({
        "order_date": ["2020-01-01", "2021-01-01", "2022-01-01"],
        "revenue": [100, 200, 300]
    })

    engine = TimeAnalyzer()
    result = engine.run(df, ["revenue"])

    assert isinstance(result, list)
    assert any("best" in msg.lower() for msg in result)
    assert any("growth" in msg.lower() for msg in result)


def test_time_analyzer_handles_missing_date_column():

    df = pd.DataFrame({
        "revenue": [100, 200, 300]
    })

    engine = TimeAnalyzer()
    result = engine.run(df, ["revenue"])

    assert isinstance(result, dict)
    assert "error" in result
