from src.ml.arguments import TrainingArguments, NotebookArguments

def test_training_arguments():
    args = TrainingArguments()
    assert type(args) == TrainingArguments

def test_notebook_arguments():
    args = NotebookArguments()
    assert type(args) == NotebookArguments