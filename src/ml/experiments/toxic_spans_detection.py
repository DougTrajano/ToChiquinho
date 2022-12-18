import mlflow
import torch
import spacy
import numpy as np
from .base import Experiment
from logger import setup_logger
from models.spacy import ToxicSpansDetectionModel
from metrics.spans import (
    precision_score,
    recall_score,
    f1_score,
)

_logger = setup_logger(__name__)

class ToxicSpansDetection(Experiment):
    name = "toxic-spans-detection"

    def __init__(self, args):
        super().__init__(args)
        spacy.util.fix_random_seed(self.args.seed)
        if spacy.prefer_gpu():
            _logger.info("Using GPU")
            torch.set_default_tensor_type("torch.cuda.FloatTensor")

        if self.args.optim == "adamw_hf":
            _logger.debug("Replacing 'adamw_hf' with 'adamw'.")
            self.args.optim = "adam"
        else:
            self.args.optim

    def init_model(self) -> ToxicSpansDetectionModel:
        self.model = ToxicSpansDetectionModel(
            spacy_model=self.args.model_name,
            toxic_label="TOXIC"
        )
        return self.model

    def run(self):
        """Run the training."""
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

            self.init_model()

            self.model.fit(
                X=self.dataset["train"]["text"],
                y=self.dataset["train"]["toxic_spans"],
                X_val=self.dataset[self.args.eval_dataset]["text"],
                y_val=self.dataset[self.args.eval_dataset]["toxic_spans"],
                eval_every=1,
                early_stopping_patience=self.args.early_stopping_patience,
                epochs=self.args.num_train_epochs,
                dropout=self.args.dropout,
                optim=self.args.optim,
                learning_rate=self.args.learning_rate,
                adam_beta1=self.args.adam_beta1,
                adam_beta2=self.args.adam_beta2,
                adam_epsilon=self.args.adam_epsilon,
                weight_decay=self.args.weight_decay,
                checkpoint_dir=self.args.checkpoint_dir,
                load_best_model_at_end=True
            )

            mlflow.log_params(
                {
                    "eval_dataset": self.args.eval_dataset,
                    "early_stopping_patience": self.args.early_stopping_patience,
                    "num_train_epochs": self.args.num_train_epochs,
                    "best_epoch": self.model.best_epoch,
                    "dropout": self.args.dropout,
                    "optim": self.args.optim,
                    "learning_rate": self.args.learning_rate,
                    "adam_beta1": self.args.adam_beta1,
                    "adam_beta2": self.args.adam_beta2,
                    "adam_epsilon": self.args.adam_epsilon,
                    "weight_decay": self.args.weight_decay
                }
            )

            # Evaluate model
            preds = self.model.predict(
                X=self.dataset[self.args.eval_dataset]["text"]
            )

            scores = {
                "eval_f1": f1_score(
                    y_true=self.dataset[self.args.eval_dataset]["toxic_spans"],
                    y_pred=preds
                ),
                "eval_precision": precision_score(
                    y_true=self.dataset[self.args.eval_dataset]["toxic_spans"],
                    y_pred=preds
                ),
                "eval_recall": recall_score(
                    y_true=self.dataset[self.args.eval_dataset]["toxic_spans"],
                    y_pred=preds
                )
            }

            _logger.info(f"Scores ({self.args.eval_dataset} set): {scores}")
            _logger.info(f"eval_f1: {scores['eval_f1']}")

            mlflow.log_metrics(scores)

            mlflow.log_figure(
                figure=self.model.plot_losses(),
                artifact_file="losses.png"
            )
            
            mlflow.log_figure(
                figure=self.model.plot_scores(),
                artifact_file="scores.png"
            )

            mlflow.spacy.log_model(
                spacy_model=self.model._model,
                artifact_path="model",
                signature=mlflow.models.signature.infer_signature(
                    np.array(self.dataset[self.args.eval_dataset]["text"]),
                    np.array(self.dataset[self.args.eval_dataset]["toxic_spans"][0])
                )
            )