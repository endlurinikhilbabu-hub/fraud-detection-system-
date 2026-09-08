import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.inference.predictor import FraudPredictor

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Real-Time Fraud Detection API",
    description="Credit card fraud detection using XGBoost",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

predictor = FraudPredictor()

# ---------------------------------------------------------
# Request Schema
# ---------------------------------------------------------

class Transaction(BaseModel):
    Time: float = Field(..., ge=0)

    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    Amount: float = Field(..., ge=0)

# ---------------------------------------------------------
# Response Schema
# ---------------------------------------------------------

class PredictionResponse(BaseModel):
    fraud_probability: float
    prediction: int
    is_fraud: bool
    threshold: float

# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "healthy",
        "model": "xgboost",
        "threshold": predictor.threshold,
    }

# ---------------------------------------------------------
# Prediction Endpoint
# ---------------------------------------------------------

@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: Transaction):

    logger.info("Prediction request received")

    try:
        features = list(transaction.model_dump().values())

        result = predictor.predict(features)

        logger.info(
            "Prediction completed | probability=%.6f | prediction=%d",
            result["fraud_probability"],
            result["prediction"],
        )

        return result

    except ValueError as exc:
        logger.warning("Prediction validation error: %s", exc)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        logger.exception("Unexpected prediction error")

        raise HTTPException(
            status_code=500,
            detail="Internal prediction error",
        )