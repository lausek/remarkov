import pytest

from io import StringIO
from typing import List

from remarkov.cli import run_command


SOURCE = """
This is a Valid Text for Building.
"""


def tokens_have_uppercase(tokens: List[str]) -> bool:
    return "".join(tokens).isupper()


def test_generating_default():
    output = run_command(
        args=["generate", "--order", "1"],
        stream=StringIO(SOURCE),
    )

    # there is at least one char that is uppercase
    assert any(map(lambda c: c.isupper(), output))


def test_generating_normalization():
    output = run_command(
        args=["generate", "--order", "1", "--normalize"],
        stream=StringIO(SOURCE),
    )

    # not one char is uppercase
    assert not any(map(lambda c: c.isupper(), output))


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
