from typing import Callable, Optional
from remarkov.model import Model
from remarkov.types import Tokenizer


def create_model(
    order: int = 1,
    tokenizer: Optional[Tokenizer] = None,
    before_insert: Optional[Callable[[str], str]] = None,
) -> "Model":
    """
    Create a new model.

    You can define the `order` of the Markov chain i.e. how many words to use for successor lookup.
    By default, remarkov will tokenize the sentence by words and punctuation. If this is not desired, you are free to provide a custom tokenizer.
    Each token is transformed using the `before_insert` callback before a token is added to the chain.
    """
    from remarkov.model import Model
    from remarkov.tokenizer import default_tokenizer

    if not tokenizer:
        tokenizer = default_tokenizer

    return Model(
        order=order,
        tokenizer=tokenizer,
        before_insert=before_insert,
    )


def load_model(path: str) -> "Model":
    """
    Loads a serialized model.
    """

    with open(path, "r") as fin:
        return parse_model(fin.read())


def parse_model(raw: str) -> "Model":
    """
    Loads a model from a JSON string.
    """

    from remarkov.model import Model

    return Model().from_json(raw)
