import logging

import pandas as pd
from feast import FeatureStore

from src.columns import TripsSource
from src.data import get_trips_dataset, train_test_split
from src.directories import directories
from src.feature_store.names import FView, TripsFeatures

# All features are used
FEATURES_TO_USE = [
    f"{FView.TEMPERATURE}:{TripsFeatures.MIN_TEMPERATURE}",
    f"{FView.TEMPERATURE}:{TripsFeatures.MAX_TEMPERATURE}",
    f"distance:{TripsFeatures.DISTANCE}",
    f"pickup_time_features:{TripsFeatures.PICKUP_HOUR}",
    f"pickup_time_features:{TripsFeatures.PICKUP_DAY}",
    f"pickup_time_features:{TripsFeatures.PICKUP_MONTH}",
]
FEATURES_COLS = list(map(lambda x: x.split(":")[1], FEATURES_TO_USE))

logger = logging.getLogger(__name__)


def _compute_target(data: pd.DataFrame) -> pd.Series:
    """Compute duration (in seconds) from trips dataset"""
    return (
        data[TripsSource.DROPOFF_DATETIME] - data[TripsSource.PICKUP_DATETIME]
    ).dt.seconds


def fetch_features(
    dataset: pd.DataFrame, *, store: FeatureStore
) -> pd.DataFrame:
    return (
        store
        .get_historical_features(dataset, features=FEATURES_TO_USE)
        .to_df()
    )[FEATURES_COLS]


def main():
    logger.info("Building training subsets...")
    train_set, test_set = (
        get_trips_dataset()
        .assign(**{
            # 'event_timestamp' is assigned for point-in-time join
            "event_timestamp": lambda x: x[TripsSource.PICKUP_DATETIME]
        })
        .sort_values(TripsSource.PICKUP_DATETIME)
        .pipe(train_test_split)
    )
    logger.info(f"Train shape:{train_set.shape}, test shape:{test_set.shape}")

    logger.info("Computing targets (trip duration)...")
    train_target = _compute_target(train_set)  # noqa: F841
    test_target = _compute_target(test_set)  # noqa: F841

    feature_store = FeatureStore(repo_path=directories.features_repo_dir)

    logger.info("Fetching features for training set...")
    train_features = fetch_features(train_set, store=feature_store)
    logger.info(f"Train features: {train_features.head()}")

    logger.info("Fetching features for testing set...")
    test_features = fetch_features(test_set, store=feature_store)
    logger.info(f"Test features: {test_features.head()}")

    logger.warning("Rest of the pipeline is not yet implemented")
