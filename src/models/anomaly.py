from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest


def train_isolation_forest(df: pd.DataFrame, contamination: float = 0.01, random_state: int = 42) -> IsolationForest:
    """Train an Isolation Forest model for anomaly detection."""
    features = df.select_dtypes(include=["number"]).copy()
    model = IsolationForest(contamination=contamination, random_state=random_state)
    model.fit(features)
    return model
