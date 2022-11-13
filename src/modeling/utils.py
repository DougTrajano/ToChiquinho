import os
import json
import torch
import numpy as np
from typing import Dict, List, Union
from transformers import EvalPrediction

from metrics import multi_label_metrics
from inference import predict
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

def preprocess_data(examples, tokenizer, max_seq_length, labels):
    """Preprocess the data.

    Args:
    - examples: The examples to preprocess.
    - tokenizer: The tokenizer to use.
    - max_seq_length: The maximum sequence length.
    - labels: The possible labels for the classification task.

    Returns:
    - The preprocessed examples.
    """
    # take a batch of texts
    text = examples["text"]

    # encode them
    encoding = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=max_seq_length
    )

    # add labels
    labels_batch = {k: examples[k] for k in examples.keys() if k in labels}

    # create numpy array of shape (batch_size, num_labels)
    labels_matrix = np.zeros((len(text), len(labels)))

    # fill numpy array
    for idx, label in enumerate(labels):
        labels_matrix[:, idx] = labels_batch[label]

    encoding["labels"] = labels_matrix.tolist()

    return encoding

def compute_metrics(p: EvalPrediction, threshold: float = 0.5) -> Dict[str, float]:
    """Compute the metrics for multi-label classification.

    Args:
    - p: The predictions of the model.

    Returns:
    - A dictionary containing the metrics (accuracy, f1, roc_auc).
    """
    preds = predict(p, threshold=threshold)
    result = multi_label_metrics(
        y_true=p.label_ids,
        y_pred=preds
    )
    return result

def prep_checkpoint_dir(checkpoint_dir: str) -> bool:
    """Prepare the checkpoint directory.

    Args:
    - checkpoint_dir: The checkpoint directory.

    Returns:
    - True if we are resuming training, False otherwise.
    """
    resume_from_checkpoint = False
    if os.path.isdir(checkpoint_dir):
        _logger.info(f"Checkpointing directory {checkpoint_dir} exists.")
        if len(os.listdir(checkpoint_dir)) == 0:
            _logger.info(f"Checkpointing directory {checkpoint_dir} is empty.")
        else:
            # Check if there "checkpoint-*" folders in the checkpointing directory.
            if len([f for f in os.listdir(checkpoint_dir) if f.startswith("checkpoint-")]) > 0:
                _logger.info(f"Checkpointing directory {checkpoint_dir} contains checkpoint-* folders.")
                resume_from_checkpoint = True
    else:
        _logger.info(f"Creating checkpointing directory {checkpoint_dir}.")
        os.mkdir(checkpoint_dir)
    return resume_from_checkpoint

def save_mlflow_checkpoint(
        mlflow_run_id: str,
        checkpoint_dir: str,
        file_name: str = "mlflow_run_id.txt") -> None:
    """Save the MLFLOW_RUN_ID to the checkpoint directory.

    Args:
    - mlflow_run_id: The MLFLOW_RUN_ID.
    - checkpoint_dir: The checkpoint directory.
    - file_name: The file name to save the MLFLOW_RUN_ID.
    """
    if not os.path.isdir(checkpoint_dir):
        os.mkdir(checkpoint_dir)

    path = os.path.join(checkpoint_dir, file_name)
    
    with open(path, "w") as f:
        f.write(mlflow_run_id)
        _logger.info(f"Saved MLFLOW_RUN_ID {mlflow_run_id} to {path}.")

def read_mlflow_checkpoint(
        checkpoint_dir: str,
        file_name: str = "mlflow_run_id.txt") -> Union[str, None]:
    """Read the MLFLOW_RUN_ID from the checkpoint directory.

    Args:
    - checkpoint_dir: The checkpoint directory.
    - file_name: The file name to save the MLFLOW_RUN_ID.

    Returns:
    - The MLFLOW_RUN_ID.
    """        
    path = os.path.join(checkpoint_dir, file_name)
    if os.path.isfile(path):
        with open(path, "r") as f:
            mlflow_run_id = f.read()
            _logger.info(f"Read MLFLOW_RUN_ID {mlflow_run_id} from {path}.")
            return mlflow_run_id

def get_sagemaker_job_name() -> Union[str, None]:
    """Get the Sagemaker job name.

    Returns:
    - The Sagemaker job name.
    """
    env = os.environ.get("SM_TRAINING_ENV", "{}")
    env = json.loads(env)
    return env.get("job_name")