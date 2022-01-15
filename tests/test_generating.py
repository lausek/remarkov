import os.path
import pytest
import tempfile

from remarkov.error import NoTransitionsDefined
from remarkov.tokenizer import token_to_lowercase
from remarkov import create_model, load_model


def is_sentence_terminator(c: str) -> bool:
    from remarkov.tokenizer import PUNCT_TERMINATION

    return c in PUNCT_TERMINATION


def test_works_without_declared_start():
    model = create_model(before_insert=token_to_lowercase)
    model.add_text("Way too simple sentence")
    assert model.generate(5).text()


def test_empty_chain_fails():
    model = create_model()

    with pytest.raises(NoTransitionsDefined):
        assert model.generate(10).text()


def test_loading_model_from_missing_file():
    with tempfile.TemporaryDirectory() as tempdir:
        fname = os.path.join(tempdir, "model.json")

        with pytest.raises(FileNotFoundError):
            load_model(fname)


def test_loading_model_from_file():
    model = create_model()
    model.add_text("This is a sample and this is another.")

    with tempfile.TemporaryDirectory() as tempdir:
        fname = os.path.join(tempdir, "model.json")

        with open(fname, "w") as tmp:
            tmp.write(model.to_json())

        loaded_model = load_model(fname)

        assert loaded_model.generate(10).text()


def test_sentence_generation_validate_amount():
    model = create_model()
    model.add_text("not empty")

    with pytest.raises(AssertionError):
        model.generate_sentences(0)

    with pytest.raises(AssertionError):
        model.generate_sentences(-1)


def test_sentence_generation_simple():
    model = create_model()
    model.add_text("A. B. C.")

    # test a few samples to avoid accidental test pass
    for i in range(1, 100 + 1):
        text = model.generate_sentences(i).text()
        assert i == len(list(filter(is_sentence_terminator, text)))


def test_sentence_generation_simple_other_termination():
    model = create_model()
    model.add_text("A? B!")

    # test a few samples to avoid accidental test pass
    for i in range(1, 100 + 1):
        text = model.generate_sentences(i).text()
        print(text)
        assert i == len(list(filter(is_sentence_terminator, text)))
