import os
from arguments import Arguments
from logger import setup_logger
from transformers import HfArgumentParser
from utils import remaining_args_to_env

_logger = setup_logger(__name__)

if __name__ == "__main__":
    parser = HfArgumentParser((Arguments))
    args, remaining_args = parser.parse_args_into_dataclasses(
        return_remaining_strings=True
    )

    _logger.info(f"Arguments: {args}")
    _logger.info(f"Remaining arguments: {remaining_args}")

    remaining_args_to_env(remaining_args)
    
    experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME")
    if experiment_name == "toxicity-type-detection":
        _logger.info("Running toxicity-type-detection experiment.")
        from experiments.toxicity_type_detection import ToxicityTypeDetection
        experiment = ToxicityTypeDetection(args)
        experiment.run()
    elif experiment_name == "toxicity-target-classification":
        _logger.info("Running toxicity-target-classification experiment.")
        from experiments.toxicity_target_classification import ToxicityTargetClassification
        experiment = ToxicityTargetClassification(args)
        experiment.run()
    else:
        _logger.error(f"Invalid experiment name: {experiment_name}.")
        raise ValueError(f"Invalid experiment name: {experiment_name}.")