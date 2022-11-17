# import os
# import shutil
from src.modeling.utils import compute_pos_weight

def test_compute_pos_weight():
    y = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    pos_weight = compute_pos_weight(y)
    assert pos_weight == [2.0, 2.0, 2.0]

# def test_prep_checkpoint_dir():
#     checkpoint_dir = "tests/checkpoints"
#     assert prep_checkpoint_dir(checkpoint_dir) == False
#     assert prep_checkpoint_dir(checkpoint_dir) == False

#     # Creating a checkpoint-* folder.
#     os.mkdir(os.path.join(checkpoint_dir, "checkpoint-1234567890"))
#     assert prep_checkpoint_dir(checkpoint_dir) == True

#     shutil.rmtree(checkpoint_dir)

# def test_save_mlflow_checkpoint():
#     mlflow_run_id = "1234567890"
#     checkpoint_dir = "tests/checkpoints"
#     prep_checkpoint_dir(checkpoint_dir)
#     save_mlflow_checkpoint(mlflow_run_id, checkpoint_dir)
#     assert resume_mlflow_checkpoint(checkpoint_dir) == mlflow_run_id
#     shutil.rmtree(checkpoint_dir)

# def test_get_sagemaker_job_name():
#     assert get_sagemaker_job_name() == None