import os
from src.ml.utils import (
    compute_pos_weight,
    remaining_args_to_env
)

def test_compute_pos_weight():
    y = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    pos_weight = compute_pos_weight(y)
    assert pos_weight == [2.0, 2.0, 2.0]

def test_remaining_args_to_env():
    args = ["--aws_profile_name", "default"]
    remaining_args_to_env(args)
    assert os.environ["AWS_PROFILE_NAME"] == "default"