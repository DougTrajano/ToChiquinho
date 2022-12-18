import os
from arguments import TrainingArguments
from logger import setup_logger
from transformers import HfArgumentParser
from utils import remaining_args_to_env

_logger = setup_logger(__name__)

if __name__ == "__main__":
    _logger.info("Starting training script.")
    
    parser = HfArgumentParser((TrainingArguments))
    args, remaining_args = parser.parse_args_into_dataclasses(
        return_remaining_strings=True
    )

    _logger.info(f"Arguments: {args}")
    _logger.info(f"Remaining arguments: {remaining_args}")

    remaining_args_to_env(remaining_args)

    experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME")
    if experiment_name == "toxicity-type-detection":
        _logger.info(f"Running {experiment_name} experiment.")
        from experiments.toxicity_type_detection import ToxicityTypeDetection
        experiment = ToxicityTypeDetection(args)
        experiment.run()
    elif experiment_name == "toxicity-target-classification":
        _logger.info(f"Running {experiment_name} experiment.")
        from experiments.toxicity_target_classification import ToxicityTargetClassification
        experiment = ToxicityTargetClassification(args)
        experiment.run()
    elif experiment_name == "toxicity-target-type-identification":
        _logger.info(f"Running {experiment_name} experiment.")
        from experiments.toxicity_target_type_identification import ToxicityTargetTypeIdentification
        experiment = ToxicityTargetTypeIdentification(args)
        experiment.run()
    elif experiment_name == "toxic-spans-detection":
        _logger.info(f"Running {experiment_name} experiment.")
        from experiments.toxic_spans_detection import ToxicSpansDetection
        experiment = ToxicSpansDetection(args)
        experiment.run()
    else:
        _logger.error(f"Invalid experiment name: {experiment_name}.")
        raise ValueError(f"Invalid experiment name: {experiment_name}.")