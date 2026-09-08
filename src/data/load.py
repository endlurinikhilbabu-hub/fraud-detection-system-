from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DATA_PATH = Path("data/raw/creditcard.csv")


def load_dataset(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the fraud dataset from disk."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    return pd.read_csv(dataset_path)
