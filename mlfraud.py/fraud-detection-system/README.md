# Fraud Detection System

A modular fraud detection project for training and evaluating machine learning models on credit card transaction data.

## Project structure

- `data/raw/` contains the original dataset
- `data/processed/` stores cleaned or transformed datasets
- `src/` contains reusable pipeline code
- `models/` saves trained artifacts
- `api/` exposes the prediction service
- `notebooks/` holds analysis and model experimentation notebooks
- `tests/` verifies core functionality

## Getting started

1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Place the raw dataset in `data/raw/creditcard.csv`.
4. Run the notebooks in order for exploration and modeling.
5. Use the API to serve predictions.

## Typical workflow

1. Load data
2. Validate schema and data quality
3. Engineer features
4. Train baseline and advanced models
5. Evaluate metrics
6. Deploy inference service
