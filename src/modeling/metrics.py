from typing import Dict
from transformers import EvalPrediction
from inference import predict
from logger import setup_logger
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score
)

_logger = setup_logger(__name__)

def compute_metrics(p: EvalPrediction,
                    threshold: float = 0.5,
                    average: str = "weighted") -> Dict[str, float]:
    """Compute the metrics for multi-label classification.

    Args:
    - p: The predictions of the model.
    - threshold: The threshold to use to convert the model's output to a label.
    - average: The average method to use for the metrics.

    Returns:
    - A dictionary containing the metrics (accuracy, f1, precision, recall).
    """
    _logger.debug(f"Computing metrics with threshold: {threshold} and average: {average}.")

    y_true = p.label_ids
    y_pred = predict(p, threshold=threshold)
    
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred, average=average),        
        "precision": precision_score(y_true, y_pred, average=average),
        "recall": recall_score(y_true, y_pred, average=average)
    }