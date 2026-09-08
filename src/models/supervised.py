from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


SUPPORTED_MODELS = {
    "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "random_forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"),
}


def split_features_target(df: pd.DataFrame, target_col: str = "Class") -> tuple[pd.DataFrame, pd.Series]:
    """Split the dataset into features and target."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y


def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    model_name: str = "logistic_regression",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train a supervised model and return the fitted model and metadata."""
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {model_name}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    model = SUPPORTED_MODELS[model_name]
    model.fit(X_train, y_train)

    return {
        "model": model,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }
