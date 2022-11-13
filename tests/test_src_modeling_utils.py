import os
import shutil
import numpy as np
from transformers import EvalPrediction
from src.modeling.utils import (
    compute_pos_weight,
    compute_metrics,
    prep_checkpoint_dir,
    save_mlflow_checkpoint,
    read_mlflow_checkpoint,
    get_sagemaker_job_name
)

def test_compute_pos_weight():
    y = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    pos_weight = compute_pos_weight(y)
    assert pos_weight == [2.0, 2.0, 2.0]

def test_compute_metrics():
    preds = np.array(
        [
            [-0.1586,  0.2220, -0.0367, -0.2293,  0.3756, -0.3352, -0.3230, -0.0227, -0.0658,  0.1569],
            [-0.1576,  0.1573, -0.0312, -0.2690,  0.3792, -0.3307, -0.3826,  0.0392, -0.1152,  0.1577]
        ]
    )

    labels = np.array(
        [
            [0., 1., 0., 0., 1., 0., 0., 0., 0., 1.],
            [0., 1., 0., 0., 1., 0., 0., 1., 0., 1.]
        ]
    )

    metrics = compute_metrics(EvalPrediction(predictions=preds, label_ids=labels))
    assert metrics == {"accuracy": 1.0, "f1": 1.0, "roc_auc": 1.0}

def test_prep_checkpoint_dir():
    checkpoint_dir = "tests/checkpoints"
    assert prep_checkpoint_dir(checkpoint_dir) == False
    assert prep_checkpoint_dir(checkpoint_dir) == False

    # Creating a checkpoint-* folder.
    os.mkdir(os.path.join(checkpoint_dir, "checkpoint-1234567890"))
    assert prep_checkpoint_dir(checkpoint_dir) == True

    shutil.rmtree(checkpoint_dir)

def test_save_mlflow_checkpoint():
    mlflow_run_id = "1234567890"
    checkpoint_dir = "tests/checkpoints"
    prep_checkpoint_dir(checkpoint_dir)
    save_mlflow_checkpoint(mlflow_run_id, checkpoint_dir)
    assert read_mlflow_checkpoint(checkpoint_dir) == mlflow_run_id
    shutil.rmtree(checkpoint_dir)

def test_get_sagemaker_job_name():
    assert get_sagemaker_job_name() == None