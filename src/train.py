import logging
from datetime import datetime
from typing import Tuple

import pandas as pd
from feast import FeatureStore
from sklearn.base import BaseEstimator

from src.columns import TripsSource
from src.config import config
from src.data import get_trips_dataset, train_test_split
from src.directories import directories
from src.feature_store.names import FService, TripsFeatures
from src.metrics import compute_metrics
from src.model import get_model, push_model

MODEL_NAME = datetime.now().strftime("%Y%m%d_%H%M")

logger = logging.getLogger(__name__)


def main():
    logger.info("Building training subsets...")
    train_set, test_set = _get_datasets()
    logger.info(f"Train shape:{train_set.shape}, test shape:{test_set.shape}")

    logger.info(f"Computing targets ({config.target})...")
    train_y, test_y = _compute_target(train_set), _compute_target(test_set)

    logger.info("Fetching features...")
    train_features, test_features = _get_features(train_set, test_set)
    logger.info(
        f"Train features: {train_features.head()}"
        f"Test features: {test_features.head()}"
    )

    logger.info("Training features...")
    model = _train_model(get_model(), features=train_features, target=train_y)

    logger.info("Evaluating model...")
    metrics = compute_metrics(model, features=test_features, target=test_y)
    logger.info(f"Metrics are: {metrics}")

    logger.info("Saving model...")
    path = push_model(model, metrics=metrics, name=MODEL_NAME)
    logger.info(f"Model saved, path: '{path}'")


def _get_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get training & testing subsets"""
    return (
        get_trips_dataset()
        .assign(**{
            # 'event_timestamp' is assigned for point-in-time join
            "event_timestamp": lambda x: x[TripsSource.PICKUP_DATETIME]
        })
        .sort_values(TripsSource.PICKUP_DATETIME)
        .pipe(train_test_split)
    )


def _compute_target(data: pd.DataFrame) -> pd.Series:
    """Compute duration (in seconds) from trips dataset"""
    return (
        data[TripsSource.DROPOFF_DATETIME] - data[TripsSource.PICKUP_DATETIME]
    ).dt.seconds


def _get_features(train_set, test_set):
    """Get features of subsets from feature store"""
    feature_store = FeatureStore(repo_path=directories.features_repo_dir)

    return (
        _fetch_features(train_set, store=feature_store),
        _fetch_features(test_set, store=feature_store)
    )


def _fetch_features(
    dataset: pd.DataFrame, *, store: FeatureStore
) -> pd.DataFrame:
    features_service = store.get_feature_service(FService.TRIP_INFOS)

    features = (
        store
        .get_historical_features(dataset, features=features_service)
        .to_df()
    )[list(TripsFeatures)]

    features.columns = features.columns.astype(str)

    return features


def _train_model(
    model: BaseEstimator, *, features: pd.DataFrame, target: pd.Series
):
    """Train model from features"""
    return model.fit(features, target)
