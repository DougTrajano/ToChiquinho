from arguments import TrainScriptArguments
from logger import setup_logger
from experiments.toxic_comment_classification import (
    ToxicCommentClassification
)

_logger = setup_logger(__name__)

class ToxicityTargetTypeIdentification(ToxicCommentClassification):
    name = "toxicity-target-type-identification"

    def __init__(self, args: TrainScriptArguments):
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
