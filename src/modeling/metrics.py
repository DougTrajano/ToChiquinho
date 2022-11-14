from typing import Any
from sklearn.metrics import (
    f1_score,
    roc_auc_score,
    accuracy_score
)


def multi_label_metrics(y_true: Any, y_pred: Any):
    """Compute the metrics for multi-label classification.
    Source: https://jesusleal.io/2021/04/21/Longformer-multilabel-classification/

    Args:
    - predictions: The predictions of the model.
    - labels: The true labels.

    Returns:
    - A dictionary containing the metrics (accuracy, f1, roc_auc).
    """
    f1_micro_average = f1_score(y_true=y_true, y_pred=y_pred, average="micro")
    roc_auc = roc_auc_score(y_true, y_pred, average="micro")
    accuracy = accuracy_score(y_true, y_pred)

    return {
        "f1": f1_micro_average,
        "roc_auc": roc_auc,
        "accuracy": accuracy
    }
