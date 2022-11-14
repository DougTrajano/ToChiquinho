import pytest
import numpy as np
from transformers.trainer_utils import PredictionOutput
from src.modeling.inference import predict

TESTS = [
    (
        np.array([[-0.1586,  0.2220, -0.0367, -0.2293,  0.3756, -0.3352, -0.3230, -0.0227, -0.0658,  0.1569]]),
        np.array([[0., 1., 0., 0., 1., 0., 0., 0., 0., 1.]]),
    ),
    (
        PredictionOutput(
            predictions=np.array([[-0.1586,  0.2220, -0.0367, -0.2293,  0.3756, -0.3352, -0.3230, -0.0227, -0.0658,  0.1569]]),
            label_ids=np.array([[0., 1., 0., 0., 1., 0., 0., 0., 0., 1.]]),
            metrics={}
        ),
        np.array([[0., 1., 0., 0., 1., 0., 0., 0., 0., 1.]]),
    ),
    (
        np.array([[-0.1576,  0.1573, -0.0312, -0.2690,  0.3792, -0.3307, -0.3826,  0.0392, -0.1152,  0.1577]]),
        np.array([[0., 1., 0., 0., 1., 0., 0., 1., 0., 1.]]),
    ),
    (
        PredictionOutput(
            predictions=np.array([[-0.1576,  0.1573, -0.0312, -0.2690,  0.3792, -0.3307, -0.3826,  0.0392, -0.1152,  0.1577]]),
            label_ids=np.array([[0., 1., 0., 0., 1., 0., 0., 1., 0., 1.]]),
            metrics={}
        ),
        np.array([[0., 1., 0., 0., 1., 0., 0., 1., 0., 1.]]),
    )
]

@pytest.mark.parametrize("predictions, expected", TESTS)
def test_predict(predictions, expected):
    assert np.array_equal(predict(predictions), expected), "The predictions are not correct."
