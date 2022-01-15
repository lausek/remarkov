import os.path
import tempfile

from io import StringIO
from typing import List
from remarkov.tokenizer import default_tokenizer

from remarkov.cli import run_command
from remarkov.model import Model


SOURCE = """
This is a Valid Text for Building.
"""


def create_test_model(order: int = 1) -> Model:
    from remarkov import create_model

    model = create_model(
        order=order,
    )

    model.add_text(SOURCE)

    return model


def save_test_model(tempdir: str, order: int = 1) -> str:
    fname = os.path.join(tempdir, "model.json")
    model = create_test_model(order=order)

    with open(fname, "w") as fout:
        fout.write(model.to_json())

    assert os.path.exists(fname)

    return fname


def tokens_have_uppercase(tokens: List[str]) -> bool:
    return "".join(tokens).isupper()


def test_generating_from_file():
    with tempfile.TemporaryDirectory() as tempdir:
        fname = save_test_model(tempdir)

        output = run_command(
            args=["generate", "--model", fname, "--words", "42"],
        )
        words = list(default_tokenizer(output))

        assert 42 == len(words), " ".join(words)


def test_generating_from_stream():
    model = create_test_model()
    output = run_command(
        args=["generate", "--words", "51"],
        stream=StringIO(model.to_json()),
    )
    words = list(default_tokenizer(output))

    assert 51 == len(words), " ".join(words)


def test_building_default_order():
    import json

    output = run_command(args=["build"], stream=StringIO(SOURCE))

    model = json.loads(output)
    assert 1 == model["order"]


def test_building_change_order():
    import json

    output = run_command(args=["build", "--order", "2"], stream=StringIO(SOURCE))

    model = json.loads(output)
    assert 2 == model["order"]


def test_building_change_order_and_normalize():
    import json

    output = run_command(
        args=["build", "--order", "2", "--normalize"], stream=StringIO(SOURCE)
    )

    model = json.loads(output)
    assert 2 == model["order"]

    # ensure that no token in the start states contains an uppercase letter
    assert not any(map(tokens_have_uppercase, model["start_states"]))


def test_building_no_compress_default():
    output = run_command(args=["build"], stream=StringIO(SOURCE))
    assert "\n" in output


def test_building_compress():
    output = run_command(args=["build", "--compress"], stream=StringIO(SOURCE))
    assert "\n" not in output


def test_building_ngrams():
    import json

    output = run_command(args=["build", "--ngrams", "3"], stream=StringIO(SOURCE))
    model = json.loads(output)

    assert model["transitions"]

    for transition in model["transitions"]:
        assert all(map(lambda token: 3 == len(token), transition["state"]))
        assert all(map(lambda token: 3 == len(token), transition["tokens"]))
