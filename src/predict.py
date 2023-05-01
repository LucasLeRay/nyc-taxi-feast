import logging

import pandas as pd
from feast import FeatureStore
from sklearn.base import BaseEstimator

from src.columns import TripsSource
from src.config import config
from src.directories import directories
from src.feature_store.names import FService, TripsFeatures
from src.model import pull_model

logger = logging.getLogger(__name__)


def main(*, model_name: str, prediction_input: str):
    """
    Make offline prediction using json input and previously trained model.
    """
    logger.info("Pulling model from registry...")
    model = pull_model(model_name)

    logger.info("Loading prediction data...")
    data = _load_data(prediction_input)

    logger.info("Fetching prediction features...")
    features = _get_features(data)

    logger.info("Predicting {config.target}...")
    prediction = _predict(model=model, features=features)

    logger.info(f"Predicted {config.target}: {prediction:.2f}")


def _load_data(prediction_input: str) -> pd.DataFrame:
    return pd.read_json(
        prediction_input,
        convert_dates=[
            TripsSource.PICKUP_DATETIME, TripsSource.DROPOFF_DATETIME
        ]
    ).assign(event_timestamp=lambda x: x[[TripsSource.PICKUP_DATETIME]])


def _get_features(prediction_set):
    """Get features of prediction set"""
    feature_store = FeatureStore(repo_path=directories.features_repo_dir)
    feature_service = feature_store.get_feature_service(FService.TRIP_INFOS)

    features = feature_store.get_historical_features(
        prediction_set, features=feature_service
    ).to_df()[list(TripsFeatures)]

    features.columns = features.columns.astype(str)

    return features


def _predict(*, model: BaseEstimator, features: pd.DataFrame) -> float:
    """Predict target from model and features"""
    return model.predict(features)[0]
