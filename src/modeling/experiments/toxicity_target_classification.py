import torch
import mlflow
import datasets
from typing import Union
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
from transformers import (
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)

# Custom code
from .base import Experiment
from arguments import Arguments
from inference import predict
from models import ToxicityTypeForSequenceClassification
from logger import setup_logger
from metrics import compute_metrics

_logger = setup_logger(__name__)

def preprocess_data(examples, tokenizer, max_seq_length):
    """Preprocess the data.

    Args:
    - examples: The examples to preprocess.
    - tokenizer: The tokenizer to use.
    - max_seq_length: The maximum sequence length.
    - labels: The possible labels for the classification task.

    Returns:
    - The preprocessed examples.
    """
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=max_seq_length
    )

class ToxicityTargetClassification(Experiment):
    name = "toxicity-target-classification"

    def __init__(self, args: Arguments):
        """Initialize the experiment.
        
        Args:
        - args: The arguments of the experiment.
        """
        super().__init__(args)
        self.classes = {
            0: "UNTARGETED",
            1: "TARGETED"
        }
        _logger.debug(f"Classes: {self.classes}")

    def init_model(self, pretrained_model_name_or_path: str):
        """Initialize the model.
        
        Args:
        - pretrained_model_name_or_path: The name or path of the pretrained model.
        
        Returns:
        - The initialized model.
        """
        _logger.info(f"Computing class weights for classes: {self.classes}.")

        # Compute class weights
        class_weights = compute_class_weight(
            class_weight="balanced",
            classes=list(self.classes.keys()),
            y=self.dataset["train"]["label"]
        ).tolist()
        mlflow.log_param("class_weights", class_weights)

        _logger.info(f"Initializing model from {pretrained_model_name_or_path}.")
        self.model = ToxicityTypeForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path,
            num_labels=len(self.classes),
            weight=torch.Tensor(class_weights).to(self.device)
        ).to(self.device)
        mlflow.log_text(str(self.model), "model_summary.txt")
        return self.model

    def prepare_dataset(self, dataset: Union[datasets.Dataset, datasets.DatasetDict]):
        """Prepare the dataset.

        Args:
        - dataset: The dataset to prepare.

        Returns:
        - The prepared dataset.
        """
        super().prepare_dataset(dataset)
        
        dataset = dataset.map(
            preprocess_data,
            remove_columns=["text"],
            batched=True,
            fn_kwargs={
                "tokenizer": self.tokenizer,
                "max_seq_length": self.args.max_seq_length
            }
        )

        return dataset

    def run(self):
        """Run the experiment."""
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
                compute_metrics=lambda p: compute_metrics(p, threshold=self.args.threshold),
                callbacks=[
                    EarlyStoppingCallback(early_stopping_patience=self.args.early_stopping_patience)
                ]
            )

            trainer.train(
                resume_from_checkpoint=self.resume_from_checkpoint
            )

            # Evaluate model
            mlflow.log_param("eval_dataset", self.args.eval_dataset)
            scores = trainer.evaluate()
            _logger.info(f"Scores ({self.args.eval_dataset} set): {scores}")
            _logger.info(f"eval_f1_weighted: {scores['eval_f1']}")

            # Classification Report
            _logger.info(f"Computing classification report.")
            preds = trainer.predict(self.dataset[self.args.eval_dataset])
            report = classification_report(
                y_true=self.dataset[self.args.eval_dataset]["label"],
                y_pred=predict(preds, threshold=self.args.threshold),
                target_names=self.classes.values(),
                digits=4, zero_division=0
            )

            mlflow.log_text(report, "classification_report.txt")