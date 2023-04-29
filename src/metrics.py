import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error


def compute_metrics(
    model: BaseEstimator, *, features: pd.DataFrame, target: pd.Series
):
    """Compute basic model metrics."""
    predicted = model.predict(features)
    return {"m2": mean_squared_error(target, predicted)}
