from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

VALID_TRANSACTION = {
    "Time": 406.0,
    "V1": -1.359807,
    "V2": -0.072781,
    "V3": 2.536347,
    "V4": 1.378155,
    "V5": -0.338321,
    "V6": 0.462388,
    "V7": 0.239599,
    "V8": 0.098698,
    "V9": 0.363787,
    "V10": 0.090794,
    "V11": -0.551600,
    "V12": -0.617801,
    "V13": -0.991390,
    "V14": -0.311169,
    "V15": 1.468177,
    "V16": -0.470400,
    "V17": 0.207971,
    "V18": 0.025791,
    "V19": 0.403993,
    "V20": 0.251412,
    "V21": -0.018307,
    "V22": 0.277838,
    "V23": -0.110474,
    "V24": 0.066928,
    "V25": 0.128539,
    "V26": -0.189115,
    "V27": 0.133558,
    "V28": -0.021053,
    "Amount": 149.62,
}

def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model"] == "xgboost"
    assert data["threshold"] == 0.56

def test_predict_valid_transaction():
    response = client.post("/predict", json=VALID_TRANSACTION)

    assert response.status_code == 200

    data = response.json()

    assert "fraud_probability" in data
    assert "prediction" in data
    assert "is_fraud" in data
    assert "threshold" in data

    assert 0 <= data["fraud_probability"] <= 1
    assert data["prediction"] in [0, 1]
    assert isinstance(data["is_fraud"], bool)
    assert data["threshold"] == 0.56

def test_predict_rejects_negative_amount():
    transaction = VALID_TRANSACTION.copy()
    transaction["Amount"] = -149.62

    response = client.post("/predict", json=transaction)

    assert response.status_code == 422

def test_predict_rejects_negative_time():
    transaction = VALID_TRANSACTION.copy()
    transaction["Time"] = -10

    response = client.post("/predict", json=transaction)

    assert response.status_code == 422

def test_predict_rejects_missing_field():
    transaction = VALID_TRANSACTION.copy()
    del transaction["V1"]

    response = client.post("/predict", json=transaction)

    assert response.status_code == 422
