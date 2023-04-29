from pathlib import Path
from typing import Dict

import joblib
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression

from src.directories import directories


def get_model() -> BaseEstimator:
    """Dummy model, used to test training & prediction"""
    return LinearRegression()


def push_model(model: BaseEstimator, *, metrics: Dict, name: str) -> Path:
    """
    Save model locally.

    Ideally, this function would push the model into a model registry, along
    with the metrics, features used to train it and the moment of training.

    We want reproducibility of experimentations, along with traceability.
    """
    path = (directories.artefacts_dir / f"{name}.pkl").resolve()
    joblib.dump(model, path)
    return path
