from logger import setup_logger
from arguments import TrainingArguments
from experiments.toxicity_target_classification import (
    ToxicityTargetClassification
)

_logger = setup_logger(__name__)

class ToxicCommentClassification(ToxicityTargetClassification):
    name = "toxic-comments-classification"

    def __init__(self, args: TrainingArguments):
        """Initialize the experiment.
        
        Args:
        - args: The arguments of the experiment.
        """
        super().__init__(args)
        self.classes = {
            0: "NOT-OFFENSIVE",
            1: "OFFENSIVE"
        }
        _logger.debug(f"Classes: {self.classes}")