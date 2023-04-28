import argparse
import logging
from enum import auto

from src.train import main as train_pipeline
from src.utils import StrEnum


class Pipeline(StrEnum):
    train = auto()


parser = argparse.ArgumentParser()
parser.add_argument("pipeline", choices=list(Pipeline))

logger = logging.getLogger(__name__)


def main(args):
    pipeline_to_function = {
        Pipeline.train: train_pipeline,
    }

    try:
        pipeline = pipeline_to_function[args.pipeline]
    except KeyError:
        logger.error(f"Pipeline '{args.pipeline}' is not implemented yet.")

    pipeline()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
