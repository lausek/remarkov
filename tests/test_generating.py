import pytest

from remarkov.error import NoTransitionsDefined, TokenStreamExhausted
from remarkov.tokenizer import token_to_lowercase
from remarkov import create_model


def test_works_without_declared_start():
    model = create_model(before_insert=token_to_lowercase)
    model.add_text("Way too simple sentence")
    assert model.generate(5).text()


def test_empty_chain_fails():
    model = create_model()

    with pytest.raises(NoTransitionsDefined):
        assert model.generate(10).text()
