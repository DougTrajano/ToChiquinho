from arguments import TrainingArguments
from logger import setup_logger
from experiments.toxicity_target_classification import (
    ToxicityTargetClassification
)

_logger = setup_logger(__name__)

class ToxicityTargetTypeIdentification(ToxicityTargetClassification):
    name = "toxicity-target-type-identification"

    def __init__(self, args: TrainingArguments):
        """Initialize the experiment.
        
        Args:
        - args: The arguments of the experiment.
        """
        super().__init__(args)

        self.classes = {
            0: "IND",
            1: "GRP",
            2: "OTH"
        }
        _logger.debug(f"Classes: {self.classes}")
