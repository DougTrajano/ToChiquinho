import os
import json
import torch
import numpy as np
from typing import List, Union
from logger import setup_logger

_logger = setup_logger(__name__)

def compute_pos_weight(
    y: Union[np.ndarray, List[List[int]], torch.Tensor]
) -> List[float]:
    """Compute positive weight for class imbalance.

    Args:
    - y: The labels.

    Returns:
    - pos_weight: array-like of shape (n_classes,)
    """
    if isinstance(y, list):
        y = np.array(y)
    elif isinstance(y, torch.Tensor):
        y = y.numpy()
        
    pos_weight = []
    for i in range(len(y[0])):
        positives = y[:, i].sum()
        negatives = len(y[:, i]) - positives
        pos_weight.append(negatives / positives)
    return pos_weight

def remaining_args_to_env(args: List[str]):
    """Convert the remaining arguments to environment variables.
    Workaround for https://github.com/boto/boto3/issues/3488

    Args:
    - args: The arguments.
    """
    _logger.debug(f"Converting remaining arguments to environment variables: {args}")
    if len(args) > 0:
        for arg in range(len(args)):
            if (
                args[arg].startswith("--")
                and args[arg] != "--MLFLOW_TAGS"
            ):
                os.environ[args[arg].strip("--")] = args[arg+1]
