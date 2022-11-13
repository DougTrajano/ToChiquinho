import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Arguments:
    data_dir: Optional[str] = field(
        default=os.environ.get("SM_CHANNEL_TRAINING"),
        metadata={
            "help": (
                "The path to the data directory. "
                "This directory should contain the training files for the dataset. "
                "If SM_CHANNEL_TRAINING environment variable is set, it will be used as the default value."
            )
        }
    )

    checkpoint_dir: Optional[str] = field(
        default="/opt/ml/checkpoints",
        metadata={
            "help": "The path the model checkpoints will be saved to."
        }
    )

    max_train_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of training examples to this "
                "value if set."
            )
        },
    )

    max_val_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of validation examples to this "
                "value if set."
            )
        },
    )

    max_test_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, truncate the number of test examples to this "
                "value if set."
            )
        },
    )

    max_seq_length: Optional[int] = field(
        default=512,
        metadata={
            "help": (
                "The maximum total input sequence length after tokenization. Sequences longer "
                "than this will be truncated, sequences shorter will be padded."
            )
        }
    )
    
    model_name: Optional[str] = field(
        default="neuralmind/bert-base-portuguese-cased",
        metadata={
            "help": "The name of the model to use. It must be a model name or a path to a directory containing model weights."
        }
    )

    num_train_epochs: Optional[int] = field(
        default=5,
        metadata={
            "help": "The number of epochs to train the model. An epoch is an iteration over the entire training set."
        }
    )

    batch_size: Optional[int] = field(
        default=8,
        metadata={
            "help": "The batch size to use for training and evaluation."
        }
    )

    adam_beta1: Optional[float] = field(
        default=0.9,
        metadata={
            "help": "The beta1 parameter for the Adam optimizer."
        }
    )

    adam_beta2: Optional[float] = field(
        default=0.999,
        metadata={
            "help": "The beta1 parameter for the Adam optimizer."
        }
    )

    adam_epsilon: Optional[float] = field(
        default=1e-8,
        metadata={
            "help": "The beta1 parameter for the Adam optimizer."
        }
    )

    learning_rate: Optional[float] = field(
        default=5e-5,
        metadata={
            "help": "The beta1 parameter for the Adam optimizer."
        }
    )

    weight_decay: Optional[float] = field(
        default=0.0,
        metadata={
            "help": "The beta1 parameter for the Adam optimizer."
        }
    )

    threshold: Optional[float] = field(
        default=0.5,
        metadata={
            "help": "The threshold to use to convert the model's output to a label."
        }
    )

    seed: Optional[int] = field(
        default=1993,
        metadata={
            "help": "The seed to use for random number generation."
        }
    )