from logger import setup_logger
from arguments import TrainScriptArguments
from experiments.toxic_comment_classification import (
    ToxicCommentClassification
)

_logger = setup_logger(__name__)

class ToxicityTargetClassification(ToxicCommentClassification):
    name = "toxicity-target-classification"

    def __init__(self, args: TrainScriptArguments):
        """Initialize the experiment.
        
        Args:
        - args: The arguments of the experiment.
        """
        super().__init__(args)
        self.classes = {
            0: "UNT",
            1: "TIN"
        }
        
        _logger.debug(f"Classes: {self.classes}")