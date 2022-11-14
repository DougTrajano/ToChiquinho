from src.modeling.arguments import Arguments

def test_arguments():
    args = Arguments()
    assert type(args) == Arguments