from __future__ import annotations

import pandas as pd


def validate_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Basic validation checks for the credit-card dataset."""
    if df.empty:
        raise ValueError("Dataset is empty.")
    required_cols = {"Time", "Amount", "Class"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df.duplicated().any():
        df = df.drop_duplicates().reset_index(drop=True)
    return df
