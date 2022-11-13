import os
import torch
import mlflow
from datasets import load_from_disk
from sklearn.metrics import classification_report
from transformers import (
    AutoTokenizer,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    set_seed
)

# Custom code
from arguments import Arguments
from inference import predict
from models import ToxicityTypeForSequenceClassification
from logger import setup_logger
from utils import (
    compute_pos_weight,
    preprocess_data,
    compute_metrics,
    prep_checkpoint_dir,
    save_mlflow_checkpoint,
    read_mlflow_checkpoint,
    get_sagemaker_job_name
)

_logger = setup_logger(__name__)


def train(args: Arguments):
    """Train the model.

    Args:
    - args: The arguments to use.
    """    
    set_seed(args.seed)

    resume_from_checkpoint = prep_checkpoint_dir(args.checkpoint_dir)
    _logger.info(f"Resume from checkpoint: {resume_from_checkpoint}")

    job_name = get_sagemaker_job_name()
    if job_name:
        args.checkpoint_dir = os.path.join(args.checkpoint_dir, job_name)

    if read_mlflow_checkpoint(args.checkpoint_dir):
        _logger.info("Resuming MLflow from checkpoint.")
        os.environ["MLFLOW_RUN_ID"] = read_mlflow_checkpoint(args.checkpoint_dir)
        if "MLFLOW_NESTED_RUN" in os.environ:
            del os.environ["MLFLOW_NESTED_RUN"]
            _logger.info("Deleted MLFLOW_NESTED_RUN from os.environ.")

    with mlflow.start_run(nested=bool(os.environ.get("MLFLOW_NESTED_RUN"))):
        # Save MLflow run ID to checkpointing directory.
        save_mlflow_checkpoint(
            mlflow_run_id=mlflow.active_run().info.run_id,
            checkpoint_dir=args.checkpoint_dir
        )
        
        dataset = load_from_disk(args.data_dir)

        for key, value in {
            "train": args.max_train_samples,
            "validation": args.max_val_samples,
            "test": args.max_test_samples
        }.items():
            if value is not None:
                dataset[key] = dataset[key].select(range(value))
                _logger.info(f"Sliced {key} dataset to {value} samples.")

        mlflow.log_param("train_size", len(dataset["train"]))
        mlflow.log_param("validation_size", len(dataset["validation"]))
        mlflow.log_param("test_size", len(dataset["test"]))

        labels = [
            label for label in dataset["train"].features.keys() if label not in ["text"]
        ]

        tokenizer = AutoTokenizer.from_pretrained(args.model_name)

        encoded_dataset = dataset.map(
            preprocess_data,
            batched=True,
            remove_columns=dataset["train"].column_names,
            fn_kwargs={
                "tokenizer": tokenizer,
                "max_seq_length": args.max_seq_length,
                "labels": labels
            }
        )

        encoded_dataset.set_format("torch")

        pos_weight = compute_pos_weight(encoded_dataset["train"]["labels"])
        mlflow.log_param("pos_weight", pos_weight)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = ToxicityTypeForSequenceClassification.from_pretrained(
            args.model_name,
            problem_type="multi_label_classification",
            num_labels=len(labels),
            id2label={idx:label for idx, label in enumerate(labels)},
            label2id={label:idx for idx, label in enumerate(labels)},
            pos_weight=torch.Tensor(pos_weight)
        ).to(device)

        mlflow.log_text(str(model), "model_summary.txt")

        trainer_args = TrainingArguments(
            output_dir=args.checkpoint_dir,
            overwrite_output_dir=True,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            learning_rate=args.learning_rate,
            weight_decay=args.weight_decay,
            adam_beta1=args.adam_beta1,
            adam_beta2=args.adam_beta2,
            adam_epsilon=args.adam_epsilon,
            per_device_train_batch_size=args.batch_size,
            per_device_eval_batch_size=args.batch_size,
            num_train_epochs=args.num_train_epochs,
            seed=args.seed
        )

        trainer = Trainer(
            model=model,
            args=trainer_args,
            train_dataset=encoded_dataset["train"],
            eval_dataset=encoded_dataset["validation"],
            tokenizer=tokenizer,
            compute_metrics=lambda p: compute_metrics(p, threshold=args.threshold),
        )

        trainer.train(
            resume_from_checkpoint=resume_from_checkpoint
        )

        # Evaluate on validation set
        val_scores = trainer.evaluate(metric_key_prefix="val_")
        _logger.info(f"Validation scores: {val_scores}")
        # mlflow.log_metrics(val_scores)
        
        # Evaluate on test set
        test_scores = trainer.evaluate(
            eval_dataset=encoded_dataset["test"],
            metric_key_prefix="test_"
        )
        _logger.info(f"Test scores: {test_scores}")
        _logger.info(f"Test F1-score: {test_scores['test_f1']}")
        # mlflow.log_metrics(test_scores)

        # Classification Report
        preds = trainer.predict(encoded_dataset["test"])
        report = classification_report(
            y_true=encoded_dataset["test"]["labels"],
            y_pred=predict(preds, threshold=args.threshold),
            target_names=labels,
            digits=4,
            zero_division=0
        )

        mlflow.log_text(report, "classification_report.txt")

if __name__ == "__main__":
    parser = HfArgumentParser((Arguments))
    args, remaining_args = parser.parse_args_into_dataclasses(
        return_remaining_strings=True
    )

    _logger.info(f"Arguments: {args}")
    _logger.info(f"Remaining arguments: {remaining_args}")

    # Workaround for https://github.com/boto/boto3/issues/3488
    # Set remaining arguments as environment variables
    if len(remaining_args) > 0:
        for arg in range(len(remaining_args)):
            if (
                remaining_args[arg].startswith("--")
                and remaining_args[arg] != "--MLFLOW_TAGS"
            ):
                os.environ[remaining_args[arg].strip("--")] = remaining_args[arg+1]

    train(args)
