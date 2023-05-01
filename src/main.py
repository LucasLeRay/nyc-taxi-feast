import logging
from enum import auto

import click

from src.predict import main as predict_pipeline
from src.train import main as train_pipeline
from src.utils import StrEnum

logger = logging.getLogger(__name__)


class Pipeline(StrEnum):
    train = auto()
    predict = auto()


@click.group()
def cli():
    ...


@cli.command(Pipeline.predict)
@click.option("--model", type=str, required=True)
@click.option("--prediction-input", type=str, required=True)
def predict(*, model, prediction_input):
    logger.info("Running prediction pipeline...")
    predict_pipeline(model_name=model, prediction_input=prediction_input)


@cli.command(Pipeline.train)
def train():
    logger.info("Running training pipeline...")
    train_pipeline()


if __name__ == "__main__":
    cli()
