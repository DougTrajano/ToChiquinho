import os
import json
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Union
from kaggle.api.kaggle_api_extended import KaggleApi
from collections.abc import MutableMapping

def download_dataset(
        output_files: Union[str, List[str]] = "train.csv",
        dataset_files: List[str] = [
            "olidbr.csv.zip",
            "train.csv",
            "test.csv",
            "train_metadata.csv",
            "test_metadata.csv",
            "additional_data.json",
            "train.json",
            "test.json"
        ]) -> Dict[str, Union[Dict, pd.DataFrame]]:
    """Download dataset from Kaggle.

    Args:
    - output_files: List of files to be outputted.
    - dataset_files: List of files to be downloaded and deleted.

    Returns:
    - A dictionary with the output files as keys and the content as values.
    """

    # Download OLID-BR dataset
    for file in dataset_files:
        if not os.path.exists(file):
            print(f"Downloading OLID-BR from Kaggle.")
            kaggle = KaggleApi()
            kaggle.authenticate()
            kaggle.dataset_download_files(dataset="olidbr", unzip=True)

    # Load data
    result = {}
    for file in output_files:
        if file.endswith(".csv"):
            result[file] = pd.read_csv(file)
        elif file.endswith(".json"):
            result[file] = json.load(open(file, "r"))
        else:
            raise ValueError(f"File {file} is not supported.")

    # Delete files
    for file in dataset_files:
        if os.path.exists(file):
            os.remove(file)

    return result

def compute_pos_weight(y: np.ndarray) -> List[float]:
    """Compute positive weight for class imbalance.

    Args:
    - y: array-like of shape (n_samples, n_classes)
    Returns:
    - pos_weight: array-like of shape (n_classes,)
    """
    pos_weight = []
    for i in range(len(y[0])):
        positives = y[:, i].sum()
        negatives = len(y[:, i]) - positives
        pos_weight.append(negatives / positives)
    return pos_weight


def flatten(d: Dict[str, Any], parent_key: str = "",
            sep: str = "_"):
    """Flatten a dictionary.

    Args:
    - d: dictionary to flatten
    - parent_key: parent key
    - sep: separator

    Returns:
    - flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
