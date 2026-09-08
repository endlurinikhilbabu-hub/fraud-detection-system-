import pandas as pd

from src.features.engineering import add_amount_features


def test_add_amount_features_creates_new_columns():
    df = pd.DataFrame({"Amount": [0.0, 1.0, 10.0]})
    result = add_amount_features(df)
    assert "amount_log1p" in result.columns
    assert "amount_rounded" in result.columns
    assert len(result) == 3
