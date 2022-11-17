import torch
import mlflow
import datasets
from typing import Union
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
from transformers import (
    Trainer,
    TrainingArguments
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

    def init_model(self, pretrained_model_name_or_path: str):
        """Initialize the model.
        
        Args:
        - pretrained_model_name_or_path: The name or path of the pretrained model.
        
        Returns:
        - The initialized model.
        """
        self.classes = {
            0: "UNTARGETED",
            1: "TARGETED"
        }

        # Compute class weights
        class_weights = compute_class_weight(
            class_weight="balanced",
            classes=list(self.classes.keys()),
            y=self.dataset["train"]["label"]
        ).tolist()
        mlflow.log_param("class_weights", class_weights)

        _logger.info(f"Initializing model from {pretrained_model_name_or_path}.")
        model = ToxicityTypeForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path,
            num_labels=len(self.classes),
            weight=torch.Tensor(class_weights).to(self.device)
        ).to(self.device)
        mlflow.log_text(str(model), "model_summary.txt")
        return model

    def prepare_dataset(self, dataset: Union[datasets.Dataset, datasets.DatasetDict]):
        """Prepare the dataset.

        Args:
        - dataset: The dataset to prepare.

        Returns:
        - The prepared dataset.
        """
        _logger.info(f"Preprocessing dataset.")
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

            self.dataset = self.load_dataset()
            self.dataset = self.slice_dataset(self.dataset)
            self.dataset = self.prepare_dataset(self.dataset)

            self.init_model(self.args.model_name)
            self.init_tokenizer(self.args.model_name)

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

            # Classification Report
            _logger.info(f"Computing classification report.")
            preds = trainer.predict(self.dataset["test"])
            report = classification_report(
                y_true=self.dataset["test"]["label"],
                y_pred=predict(preds, threshold=self.args.threshold),
                target_names=self.classes.values(),
                digits=4, zero_division=0
            )

            mlflow.log_text(report, "classification_report.txt")