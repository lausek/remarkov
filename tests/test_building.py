import pytest

from remarkov.error import NoTransitionsDefined, TokenStreamExhausted
from remarkov.prelude import ReMarkov, token_to_lowercase, token_to_uppercase


def test_before_insert_disabled():
    remarkov = ReMarkov(before_insert=None)
    remarkov.add_text("I have a dream.")

    for key in ["I", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_before_insert():
    remarkov = ReMarkov(before_insert=token_to_uppercase)
    remarkov.add_text("I have a dream.")

    for key in ["I", "HAVE", "A", "DREAM"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_transitions_simple():
    remarkov = ReMarkov(before_insert=token_to_lowercase)
    remarkov.add_text("I HaVe A dReAm.")

    for key in ["i", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_order_too_big():
    remarkov = ReMarkov(order=6)

    with pytest.raises(TokenStreamExhausted):
        remarkov.add_text("A b c d e")

    with pytest.raises(NoTransitionsDefined):
        remarkov.add_text("A b c d e f")
        remarkov.generate(10).text()
