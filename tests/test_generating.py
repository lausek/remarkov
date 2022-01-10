import os.path
import pytest
import tempfile

from remarkov.error import NoTransitionsDefined, TokenStreamExhausted
from remarkov.tokenizer import token_to_lowercase
from remarkov import create_model, load_model


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
