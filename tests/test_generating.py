import pytest

from remarkov.error import NoTransitionsDefined, TokenStreamExhausted
from remarkov.prelude import ReMarkov, token_to_lowercase, token_to_uppercase


def test_works_without_declared_start():
    remarkov = ReMarkov(before_insert=token_to_lowercase)
    remarkov.add_text("Way too simple sentence")
    assert remarkov.generate(5).text()


def test_empty_chain_fails():
    remarkov = ReMarkov()

    with pytest.raises(NoTransitionsDefined):
        assert remarkov.generate(10).text()
