import os
import json
import torch
import mlflow
import datasets
import warnings
from typing import Union
from transformers import (
    AutoTokenizer,
    PreTrainedModel,
    Trainer,
    TrainingArguments,
    set_seed
)

# Custom code
from arguments import Arguments
from logger import setup_logger
from metrics import compute_metrics

_logger = setup_logger(__name__)

class Experiment(object):
    name = "Experiment"

    def __init__(self, args: Arguments):
        """Initialize the experiment.
        
        Args:
        - args: The arguments.
        """
        self.args = args
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.job_name = self.get_sagemaker_job_name()

    def __str__(self):
        """String representation of the experiment."""
        return self.name

    def init_experiment(self):
        """Run the experiment."""
        _logger.info(f"Initializing experiment {self.name}.")

        set_seed(self.args.seed)

        self.resume_from_checkpoint = self.prep_checkpoint_dir(self.args.checkpoint_dir)
        _logger.info(f"Resume from checkpoint: {self.resume_from_checkpoint}")
 
        if self.job_name:
            self.args.checkpoint_dir = os.path.join(self.args.checkpoint_dir, self.job_name)

        if self.resume_mlflow_checkpoint(self.args.checkpoint_dir):
            _logger.info("Resuming MLflow from checkpoint.")
            os.environ["MLFLOW_RUN_ID"] = self.resume_mlflow_checkpoint(self.args.checkpoint_dir)

        self.nested_run = bool(
            os.environ.get("MLFLOW_RUN_ID")
            and not self.resume_mlflow_checkpoint(self.args.checkpoint_dir)
        )

        if os.environ.get("MLFLOW_RUN_ID"):
            mlflow.start_run()

    def init_model(self, pretrained_model_name_or_path: str):
        """Initialize the model.
        
        Args:
        - pretrained_model_name_or_path: The pretrained model name or path.
        
        Returns:
        - The model.
        """
        _logger.info(f"Initializing model from {pretrained_model_name_or_path}.")
        self.model = PreTrainedModel.from_pretrained(
            pretrained_model_name_or_path
        ).to(self.device)
        mlflow.log_text(str(self.model), "model_summary.txt")
        return self.model

    def init_tokenizer(self, pretrained_model_name_or_path: str):
        """Initialize the tokenizer.

        Args:
        - pretrained_model_name_or_path: The pretrained model name or path.

        Returns:
        - The tokenizer.
        """
        _logger.info(f"Initializing tokenizer from {pretrained_model_name_or_path}.")
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
        return self.tokenizer

    def load_dataset(self):
        """Load the dataset."""
        _logger.info(f"Loading dataset from {self.args.data_dir}.")
        dataset = datasets.load_from_disk(self.args.data_dir)
        return dataset

    def slice_dataset(self, dataset: Union[datasets.Dataset, datasets.DatasetDict]):
        """Slice the dataset.

        Args:
        - dataset: The dataset.

        Returns:
        - The sliced dataset.
        """
        _logger.info(f"Slicing dataset.")

        max_samples = {
            "train": self.args.max_train_samples,
            "validation": self.args.max_val_samples,
            "test": self.args.max_test_samples
        }

        for key, value in max_samples.items():
            if value is not None:
                dataset[key] = dataset[key].select(range(value))
                _logger.info(f"Sliced {key} dataset to {value} samples.")
        
        for split in dataset.keys():
            mlflow.log_param(f"{split}_size", len(dataset[split]))

        _logger.info(f"Dataset: {dataset}")
        return dataset

    def prepare_dataset(self, dataset: Union[datasets.Dataset, datasets.DatasetDict]):
        """Prepare the dataset.

        Args:
        - dataset: The dataset.

        Returns:
        - The prepared dataset.
        """
        warnings.warn("prepare_dataset() not implemented.")
        return dataset

    def prep_checkpoint_dir(self, checkpoint_dir: str) -> bool:
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
        self,
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

    def resume_mlflow_checkpoint(
        self,
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

    def get_sagemaker_job_name(self) -> Union[str, None]:
        """Get the Sagemaker job name.

        Returns:
        - The Sagemaker job name.
        """
        env = os.environ.get("SM_TRAINING_ENV", "{}")
        env = json.loads(env)
        return env.get("job_name")

    def run(self):
        """Run the training."""
        self.init_experiment()
        with mlflow.start_run(nested=self.nested_run):
            # Save MLflow run ID to checkpointing directory.
            self.save_mlflow_checkpoint(
                mlflow_run_id=mlflow.active_run().info.run_id,
                checkpoint_dir=self.args.checkpoint_dir
            )

            self.init_tokenizer(self.args.model_name)
            
            self.dataset = self.load_dataset()
            self.dataset = self.slice_dataset(self.dataset)
            self.dataset = self.prepare_dataset(self.dataset)

            self.init_model(self.args.model_name)

            self.dataset.set_format("torch")

            trainer_args = TrainingArguments(
                output_dir=self.args.checkpoint_dir,
                overwrite_output_dir=True,
                evaluation_strategy="epoch",
                save_strategy="epoch",
                load_best_model_at_end=True,
                metric_for_best_model="f1",
                learning_rate=self.args.learning_rate,
                weight_decay=self.args.weight_decay,
                adam_beta1=self.args.adam_beta1,
                adam_beta2=self.args.adam_beta2,
                adam_epsilon=self.args.adam_epsilon,
                per_device_train_batch_size=self.args.batch_size,
                per_device_eval_batch_size=self.args.batch_size,
                num_train_epochs=self.args.num_train_epochs,
                seed=self.args.seed
            )

            trainer = Trainer(
                model=self.model,
                args=trainer_args,
                train_dataset=self.dataset["train"],
                eval_dataset=self.dataset["validation"],
                tokenizer=self.tokenizer,
                compute_metrics=lambda p: compute_metrics(p, threshold=self.args.threshold),
            )

            trainer.train(
                resume_from_checkpoint=self.resume_from_checkpoint
            )

            # Evaluate on validation set
            val_scores = trainer.evaluate(metric_key_prefix="val")
            _logger.info(f"Validation scores: {val_scores}")
            
            # Evaluate on test set
            test_scores = trainer.evaluate(
                eval_dataset=self.dataset["test"],
                metric_key_prefix="test"
            )

            _logger.info(f"Test scores: {test_scores}")
            _logger.info(f"Test F1-score: {test_scores['test_f1']}")