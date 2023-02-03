import os
import json
import torch
import mlflow
import datasets
import matplotlib.pyplot as plt
from collections import OrderedDict
from typing import Union, Dict, List
from transformers import (
    AutoTokenizer,
    EarlyStoppingCallback,
    PreTrainedModel,
    Trainer,
    TrainingArguments as HfTrainingArguments,
    set_seed
)

# Custom code
from arguments import TrainingArguments
from logger import setup_logger
from metrics.utils import compute_metrics

_logger = setup_logger(__name__)

class Experiment(object):
    name = "base-experiment"

    def __init__(self, args: TrainingArguments):
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
        _logger.debug(f"Nested run: {self.nested_run}")
        
        if os.environ.get("MLFLOW_RUN_ID") and self.nested_run:
            mlflow.start_run()
            _logger.debug(f"Starting mlflow run: {mlflow.active_run().info.run_id}")

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
        max_samples = {
            "train": self.args.max_train_samples,
            "validation": self.args.max_val_samples,
            "test": self.args.max_test_samples
        }

        if not any(max_samples.values()):
            return dataset

        _logger.info(f"Slicing dataset.")
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
        _logger.info(f"Preparing dataset.")

        # Concatenate the train and validation sets to create a new train set.
        if (
            self.args.concat_validation_set
            and self.args.eval_dataset != "validation"
            and "train" in dataset.keys()
            and "validation" in dataset.keys()
        ):
            _logger.info(f"Concatenating validation set to train set.")
            self.dataset["train"] = datasets.concatenate_datasets(
                [
                    self.dataset["train"],
                    self.dataset["validation"]
                ]
            )

            # Drop validation
            

        _logger.info(f"Dataset: {dataset}")
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

    def plot_hf_metrics(
        self,
        log_history: List[Dict[str, float]],
        metrics: Dict[str, str] = {
            "eval_accuracy": "Accuracy",
            "eval_f1": "F1-score",
            "eval_precision": "Precision",
            "eval_recall": "Recall"
        },
        xtitle: str = "Epoch",
        ytitle: str = "Scores") -> plt.Figure:
        """Plot the Hugging Face metrics.

        Args:
        - log_history: The Hugging Face log history.
        - metrics: The metrics to plot (key: metric name, value: plot title).
        - xtitle: The x-axis title.
        - ytitle: The y-axis title.

        Returns:
        - The plot.
        """
        _logger.debug(
            {
                "log_history": log_history,
                "metrics": metrics,
                "xtitle": xtitle,
                "ytitle": ytitle
            }
        )

        # Prepare the metrics
        _metrics = OrderedDict()
        for item in log_history:
            epoch = int(item["epoch"])
            for key, value in item.items():
                if key in metrics:
                    if epoch not in _metrics:
                        _metrics[epoch] = {}
                    _metrics[epoch][key] = value

        fig = plt.figure(figsize=(10, 6))
        for key, value in metrics.items():
            data = [_metrics[i][key] for i in _metrics if key in _metrics[i]]
            if len(data) == 0:
                raise ValueError(
                    f"{key} is not in the metrics. Metrics: {_metrics}.")
            plt.plot(data, label=value)

        plt.xticks(range(len(_metrics)), range(1, len(_metrics) + 1))
        plt.ylim(0, 1)
        plt.xlabel(xtitle)
        plt.ylabel(ytitle)
        plt.legend()

        return fig

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

            trainer_args = HfTrainingArguments(
                output_dir=self.args.checkpoint_dir,
                overwrite_output_dir=True,
                evaluation_strategy="epoch",
                save_strategy="epoch",
                save_total_limit=5,
                load_best_model_at_end=True,
                metric_for_best_model="f1",
                learning_rate=self.args.learning_rate,
                weight_decay=self.args.weight_decay,
                adam_beta1=self.args.adam_beta1,
                adam_beta2=self.args.adam_beta2,
                adam_epsilon=self.args.adam_epsilon,
                label_smoothing_factor=self.args.label_smoothing_factor,
                optim=self.args.optim,
                per_device_train_batch_size=self.args.batch_size,
                per_device_eval_batch_size=self.args.batch_size,
                num_train_epochs=self.args.num_train_epochs,
                seed=self.args.seed
            )

            trainer = Trainer(
                model=self.model,
                args=trainer_args,
                train_dataset=self.dataset["train"],
                eval_dataset=self.dataset[self.args.eval_dataset],
                tokenizer=self.tokenizer,
                compute_metrics=lambda p: compute_metrics(p, threshold=self.args.threshold, problem_type="multi-class"),
                callbacks=[
                    EarlyStoppingCallback(early_stopping_patience=self.args.early_stopping_patience)
                ] if self.args.early_stopping_patience is not None else None
            )

            trainer.train(
                resume_from_checkpoint=self.resume_from_checkpoint
            )

            # Evaluate model
            mlflow.log_param("eval_dataset", self.args.eval_dataset)
            scores = trainer.evaluate()
            _logger.info(f"Scores ({self.args.eval_dataset} set): {scores}")
            _logger.info(f"eval_f1_weighted: {scores['eval_f1']}")

            # Plot metrics
            _logger.info(f"Plotting scores.")
            mlflow.log_figure(
                figure=self.plot_hf_metrics(
                    log_history=trainer.state.log_history
                ),
                artifact_file="scores.png"
            )

            # Plot loss
            _logger.info(f"Plotting losses.")
            mlflow.log_figure(
                figure=self.plot_hf_metrics(
                    log_history=trainer.state.log_history,
                    metrics={"eval_loss": "Loss"},
                    xtitle="Epoch",
                    ytitle="Loss"
                ),
                artifact_file="losses.png"
            )

            mlflow.log_dict(
                dictionary=trainer.state.log_history,
                artifact_file="log_history.json"
            )

        _logger.info(f"Experiment completed.")