import pandas as pd

from src.data.load import load_dataset
from src.data.validation import validate_dataset


def test_validate_dataset_accepts_expected_columns():
    df = pd.DataFrame(
        {
            "Time": [0, 1, 2],
            "Amount": [10.0, 20.0, 30.0],
            "Class": [0, 1, 0],
        }
    )
    validated = validate_dataset(df)
    assert list(validated.columns) == ["Time", "Amount", "Class"]
    assert len(validated) == 3


def test_load_dataset_raises_when_missing():
    try:
        load_dataset("missing.csv")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError")
