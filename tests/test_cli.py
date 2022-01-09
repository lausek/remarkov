from io import StringIO

from remarkov.cli import run_generation


def test_generating_default():
    source = """
    Please Keep The Caps here.
    """

    output = run_generation(
        args=["--order", "1"],
        stream=StringIO(source),
    )

    # there is at least one char that is uppercase
    assert any(map(lambda c: c.isupper(), output))


def test_normalization():
    source = """
    Please Keep the Caps here.
    """

    output = run_generation(
        args=["--order", "1", "--normalize"],
        stream=StringIO(source),
    )

    # not one char is uppercase
    assert not any(map(lambda c: c.isupper(), output))
