import torch
import numpy as np
from typing import Union
from transformers import EvalPrediction
from transformers.trainer_utils import PredictionOutput


def predict(
        predictions: Union[EvalPrediction, PredictionOutput, np.ndarray],
        return_proba: bool = False,
        threshold: float = 0.5):
    """Predict the labels of a batch of samples.

    Args:
    - predictions: The predictions of the model.
    - return_proba: Whether to return the probability of each label.
    - threshold: The threshold to be used to convert the logits to labels.

    Returns:
    - The predicted labels.
    """
    if isinstance(predictions, (EvalPrediction, PredictionOutput)):
        if isinstance(predictions.predictions, tuple):
            predictions = predictions.predictions[0]
        else:
            predictions = predictions.predictions

    # first, apply sigmoid on predictions which are of shape (batch_size, num_labels)
    sigmoid = torch.nn.Sigmoid()
    probs: np.ndarray = sigmoid(torch.Tensor(predictions))

    if return_proba:
        return probs
    else:
        # use threshold to turn them into integer predictions
        y_pred = np.zeros(probs.shape)
        y_pred[np.where(probs >= threshold)] = 1
        return y_pred
