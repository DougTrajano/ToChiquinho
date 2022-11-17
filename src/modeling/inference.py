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

    # Check if the predictions are binary
    if predictions.shape[1] == 2:
        act_func = torch.nn.Softmax(dim=1)
    else:
        # first, apply sigmoid on predictions which are of shape (batch_size, num_labels)
        act_func = torch.nn.Sigmoid()

    probs: np.ndarray = act_func(torch.Tensor(predictions))
            
    if return_proba:
        return probs
    else:
        if predictions.shape[1] == 2:
            return np.array(probs[:, 1] > threshold, dtype=int)
        # use threshold to turn them into integer predictions
        y_pred = np.zeros(probs.shape)
        y_pred[np.where(probs >= threshold)] = 1
        return y_pred