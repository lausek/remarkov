import pytest

from remarkov.tokenizer import create_ngram_tokenizer, default_tokenizer


def test_default_tokenizer_empty_input():
    token_stream = default_tokenizer("")
    assert not list(token_stream)


def test_default_tokenizer_sentence():
    token_stream = default_tokenizer("I have a dream.")
    assert ["I", "have", "a", "dream", "."] == list(token_stream)


def test_default_tokenizer_colon():
    token_stream = default_tokenizer("Say:Hello")
    assert ["Say", ":", "Hello"] == list(token_stream)


def test_default_tokenizer_interpunction():
    token_stream = default_tokenizer("What??No way!Anyways, well")
    assert ["What", "?", "?", "No", "way", "!", "Anyways", ",", "well"] == list(
        token_stream
    )


def test_default_tokenizer_parens():
    token_stream = default_tokenizer("As seen in.(link it)")
    assert ["As", "seen", "in", ".", "(", "link", "it", ")"] == list(token_stream)


def test_default_tokenizer_brackets():
    token_stream = default_tokenizer("Insert [Footnote here]")
    assert ["Insert", "[", "Footnote", "here", "]"] == list(token_stream)


def test_default_tokenizer_quotes():
    token_stream = default_tokenizer('"Avoid this now"')
    assert ['"', "Avoid", "this", "now", '"'] == list(token_stream)


def test_default_tokenizer_stripping_spaces():
    token_stream = default_tokenizer("  Way     too much     space   here  ")
    assert ["Way", "too", "much", "space", "here"] == list(token_stream)


def test_default_tokenizer_remove_newline():
    token_stream = default_tokenizer("A\nB\n\nC\n\r\nD")
    assert ["A", "B", "C", "D"] == list(token_stream)


def test_ngram_tokenizer():
    ngram1_tokenizer = create_ngram_tokenizer(1)
    token_stream = ngram1_tokenizer("AbcdEf")
    assert ["A", "b", "c", "d", "E", "f"] == list(token_stream)


def test_ngram2_tokenizer():
    ngram2_tokenizer = create_ngram_tokenizer(2)
    token_stream = ngram2_tokenizer("AbcdEf")
    assert ["Ab", "cd", "Ef"] == list(token_stream)


def test_ngram_tokenizer_padding():
    ngram3_tokenizer = create_ngram_tokenizer(3)
    token_stream = ngram3_tokenizer("AaBBcde")
    assert ["AaB", "Bcd", "e  "] == list(token_stream)


def test_ngram_invalid_length():
    with pytest.raises(AssertionError):
        create_ngram_tokenizer(0)
