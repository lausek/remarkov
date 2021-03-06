import pytest

from remarkov.error import NoTransitionsDefined, TokenStreamExhausted
from remarkov.tokenizer import token_to_lowercase, token_to_uppercase
from remarkov import create_model, parse_model


def test_before_insert_disabled():
    model = create_model(before_insert=None)
    model.add_text("I have a dream.")

    for key in ["I", "have", "a", "dream"]:
        assert (key,) in model.transitions

    assert (".",) not in model.transitions


def test_before_insert():
    model = create_model(before_insert=token_to_uppercase)
    model.add_text("I have a dream.")

    for key in ["I", "HAVE", "A", "DREAM"]:
        assert (key,) in model.transitions

    assert (".",) not in model.transitions


def test_transitions_simple():
    model = create_model(before_insert=token_to_lowercase)
    model.add_text("I HaVe A dReAm.")

    for key in ["i", "have", "a", "dream"]:
        assert (key,) in model.transitions

    assert (".",) not in model.transitions


def test_order_too_big():
    model = create_model(order=6)

    with pytest.raises(TokenStreamExhausted):
        model.add_text("A b c d e")

    with pytest.raises(NoTransitionsDefined):
        model.add_text("A b c d e f")
        model.generate(10).text()


def test_initial_state_is_start_state():
    model = create_model(order=2)
    model.add_text("This works now.")

    assert 1 == len(model.transitions.start_states)
