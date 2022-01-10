from typing import Callable, Optional
from remarkov.model import ReMarkovModel
from remarkov.types import Tokenizer
from remarkov.tokenizer import default_tokenizer


def create_model(
    order: int = 1,
    tokenizer: Tokenizer = default_tokenizer,
    before_insert: Optional[Callable[[str], str]] = None,
) -> "ReMarkovModel":
    from remarkov.model import ReMarkovModel

    return ReMarkovModel(
        order=order,
        tokenizer=tokenizer,
        before_insert=before_insert,
    )


def load_model(path: str) -> "ReMarkovModel":
    with open(path, "r") as fin:
        return parse_model(fin.read())


def parse_model(raw: str) -> "ReMarkovModel":
    from remarkov.model import ReMarkovModel

    return ReMarkovModel().from_json(raw)
