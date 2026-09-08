from pathlib import Path
import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "xgboost_fraud_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"
THRESHOLD_PATH = BASE_DIR / "models" / "threshold.txt"


class FraudPredictor:
    """
    Production inference class for fraud detection.

    Responsibilities:
    1. Load the trained XGBoost model.
    2. Load the scaler for feature normalization.
    3. Load the selected classification threshold.
    4. Accept transaction features.
    5. Generate fraud probability.
    6. Convert probability into fraud/legitimate decision.
    """

    def __init__(self):
        """Load model, scaler, and threshold."""

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}"
            )

        if not SCALER_PATH.exists():
            raise FileNotFoundError(
                f"Scaler not found at {SCALER_PATH}"
            )

        if not THRESHOLD_PATH.exists():
            raise FileNotFoundError(
                f"Threshold not found at {THRESHOLD_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)
        self.scaler = joblib.load(SCALER_PATH)

        with open(THRESHOLD_PATH, "r") as file:
            self.threshold = float(file.read().strip())

    def predict(self, features):
        """
        Predict whether a transaction is fraudulent.

        Parameters
        ----------
        features : array-like
            Transaction features in the same order used during training.

        Returns
        -------
        dict
            Fraud probability and classification result.
        """

        # Convert input to numpy array
        features = np.asarray(features, dtype=float)

        # Ensure one transaction is represented as one row
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Validate number of features
        expected_features = self.model.n_features_in_

        if features.shape[1] != expected_features:
            raise ValueError(
                f"Expected {expected_features} features, "
                f"got {features.shape[1]}"
            )

        # Scale features using training scaler
        feature_names = [
            "Time",
            "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
            "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19",
            "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28",
            "Amount"
        ]

        features_df = pd.DataFrame(features, columns=feature_names)

        features_scaled = self.scaler.transform(features_df)

        # Generate fraud probability
        probability = self.model.predict_proba(
            features_scaled
        )[0, 1]

        # Apply saved threshold
        prediction = int(
            probability >= self.threshold
        )

        return {
            "fraud_probability": float(probability),
            "prediction": prediction,
            "is_fraud": bool(prediction),
            "threshold": float(self.threshold)
        }