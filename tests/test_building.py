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


def test_initial_state_is_start_state():
    remarkov = ReMarkov(order=2)
    remarkov.add_text("This works now.")

    assert 1 == len(remarkov.transitions.start_states)


def test_json_serialization():
    import json

    remarkov = ReMarkov()
    remarkov.add_text(
        "This is a sample and this is another. Be sure to have multiple. Sentences."
    )

    assert json.loads(remarkov.to_json())


def test_json_persistance():
    remarkov = ReMarkov(order=2)
    remarkov.add_text(
        "This is a sample and this is another. Be sure to have multiple. Sentences."
    )

    source_model = remarkov.to_json()
    loaded_remarkov = ReMarkov.from_json(source_model)

    print(remarkov.transitions.start_states)

    assert 2 == loaded_remarkov.order
    assert loaded_remarkov.transitions
    assert 2 == len(loaded_remarkov.transitions.start_states)
