from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_predict_valid_transaction():
    payload = {
        "Time": 0.0,
        "V1": 0.0,
        "V2": 0.0,
        "V3": 0.0,
        "V4": 0.0,
        "V5": 0.0,
        "V6": 0.0,
        "V7": 0.0,
        "V8": 0.0,
        "V9": 0.0,
        "V10": 0.0,
        "V11": 0.0,
        "V12": 0.0,
        "V13": 0.0,
        "V14": 0.0,
        "V15": 0.0,
        "V16": 0.0,
        "V17": 0.0,
        "V18": 0.0,
        "V19": 0.0,
        "V20": 0.0,
        "V21": 0.0,
        "V22": 0.0,
        "V23": 0.0,
        "V24": 0.0,
        "V25": 0.0,
        "V26": 0.0,
        "V27": 0.0,
        "V28": 0.0,
        "Amount": 0.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "fraud_probability" in data
    assert "prediction" in data
    assert "is_fraud" in data
    assert "threshold" in data

    assert isinstance(data["fraud_probability"], float)
    assert data["prediction"] in [0, 1]
    assert isinstance(data["is_fraud"], bool)
    assert data["threshold"] == 0.56


def test_prediction_consistency():
    payload = {
        "Time": 0.0,
        "V1": 0.0,
        "V2": 0.0,
        "V3": 0.0,
        "V4": 0.0,
        "V5": 0.0,
        "V6": 0.0,
        "V7": 0.0,
        "V8": 0.0,
        "V9": 0.0,
        "V10": 0.0,
        "V11": 0.0,
        "V12": 0.0,
        "V13": 0.0,
        "V14": 0.0,
        "V15": 0.0,
        "V16": 0.0,
        "V17": 0.0,
        "V18": 0.0,
        "V19": 0.0,
        "V20": 0.0,
        "V21": 0.0,
        "V22": 0.0,
        "V23": 0.0,
        "V24": 0.0,
        "V25": 0.0,
        "V26": 0.0,
        "V27": 0.0,
        "V28": 0.0,
        "Amount": 0.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    probability = result["fraud_probability"]
    prediction = result["prediction"]
    threshold = result["threshold"]

    expected_prediction = int(probability >= threshold)

    assert prediction == expected_prediction
    assert result["is_fraud"] == (prediction == 1)


import pandas as pd
from sklearn.model_selection import train_test_split

from src.inference.predictor import FraudPredictor


def load_test_data():
    df = pd.read_csv("data/raw/creditcard.csv")

    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=42,
        stratify=y_temp
    )

    return X_test, y_test


def test_real_legitimate_transaction():
    X_test, y_test = load_test_data()

    # Select an actual legitimate transaction
    sample = X_test[y_test == 0].iloc[0]

    payload = sample.to_dict()

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    # The transaction is actually legitimate
    assert y_test.loc[sample.name] == 0

    # API should return a valid prediction
    assert result["prediction"] in [0, 1]

    # API output must follow its threshold
    expected_prediction = int(
        result["fraud_probability"] >= result["threshold"]
    )

    assert result["prediction"] == expected_prediction


def test_real_fraud_transaction():
    X_test, y_test = load_test_data()

    # Select an actual fraudulent transaction
    sample = X_test[y_test == 1].iloc[0]

    payload = sample.to_dict()

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    # The transaction is actually fraudulent
    assert y_test.loc[sample.name] == 1

    # API should return a valid prediction
    assert result["prediction"] in [0, 1]

    # API output must follow its threshold
    expected_prediction = int(
        result["fraud_probability"] >= result["threshold"]
    )

    assert result["prediction"] == expected_prediction


def test_api_predictor_consistency():
    X_test, y_test = load_test_data()

    predictor = FraudPredictor()

    sample = X_test[y_test == 1].iloc[0]

    features = sample.tolist()

    direct_result = predictor.predict(features)

    response = client.post(
        "/predict",
        json=sample.to_dict()
    )

    assert response.status_code == 200

    api_result = response.json()

    assert abs(
        direct_result["fraud_probability"]
        - api_result["fraud_probability"]
    ) < 1e-10

    assert direct_result["prediction"] == api_result["prediction"]


def test_predict_missing_feature():
    payload = {
        "Time": 0.0,
        "V1": 0.0,
        "V2": 0.0,
        "V3": 0.0,
        "V4": 0.0,
        "V5": 0.0,
        "V6": 0.0,
        "V7": 0.0,
        "V8": 0.0,
        "V9": 0.0,
        "V10": 0.0,
        "V11": 0.0,
        "V12": 0.0,
        "V13": 0.0,
        "V14": 0.0,
        "V15": 0.0,
        "V16": 0.0,
        "V17": 0.0,
        "V18": 0.0,
        "V19": 0.0,
        "V20": 0.0,
        "V21": 0.0,
        "V22": 0.0,
        "V23": 0.0,
        "V24": 0.0,
        "V25": 0.0,
        "V26": 0.0,
        "V27": 0.0,
        # V28 intentionally missing
        "Amount": 0.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_wrong_data_type():
    payload = {
        "Time": "not-a-number",
        "V1": 0.0,
        "V2": 0.0,
        "V3": 0.0,
        "V4": 0.0,
        "V5": 0.0,
        "V6": 0.0,
        "V7": 0.0,
        "V8": 0.0,
        "V9": 0.0,
        "V10": 0.0,
        "V11": 0.0,
        "V12": 0.0,
        "V13": 0.0,
        "V14": 0.0,
        "V15": 0.0,
        "V16": 0.0,
        "V17": 0.0,
        "V18": 0.0,
        "V19": 0.0,
        "V20": 0.0,
        "V21": 0.0,
        "V22": 0.0,
        "V23": 0.0,
        "V24": 0.0,
        "V25": 0.0,
        "V26": 0.0,
        "V27": 0.0,
        "V28": 0.0,
        "Amount": 0.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_missing_amount():
    payload = {
        "Time": 0.0,
        "V1": 0.0,
        "V2": 0.0,
        "V3": 0.0,
        "V4": 0.0,
        "V5": 0.0,
        "V6": 0.0,
        "V7": 0.0,
        "V8": 0.0,
        "V9": 0.0,
        "V10": 0.0,
        "V11": 0.0,
        "V12": 0.0,
        "V13": 0.0,
        "V14": 0.0,
        "V15": 0.0,
        "V16": 0.0,
        "V17": 0.0,
        "V18": 0.0,
        "V19": 0.0,
        "V20": 0.0,
        "V21": 0.0,
        "V22": 0.0,
        "V23": 0.0,
        "V24": 0.0,
        "V25": 0.0,
        "V26": 0.0,
        "V27": 0.0,
        "V28": 0.0,
        # Amount intentionally missing
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    