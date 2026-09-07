from __future__ import annotations

import pandas as pd


def add_amount_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create basic transaction-derived features from the Amount column."""
    out = df.copy()
    out["amount_log1p"] = out["Amount"].apply(lambda x: __import__("math").log1p(x))
    out["amount_rounded"] = out["Amount"].round(2)
    return out
