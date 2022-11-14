import numpy as np
from src.modeling.metrics import multi_label_metrics

def test_multi_label_metrics():
    y_true = np.array([[0., 1., 0., 0., 1., 0., 0., 0., 0., 1.]])
    y_pred = np.array([[0., 1., 0., 0., 1., 0., 0., 0., 0., 1.]])
    expected = {
        "f1": 1.0,
        "roc_auc": 1.0,
        "accuracy": 1.0
    }
    assert multi_label_metrics(y_true, y_pred) == expected, "The metrics are not correct."