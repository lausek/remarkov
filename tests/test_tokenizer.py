from remarkov.tokenizer import default_tokenizer


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


def test_default_tokenizer_stripping_spaces():
    token_stream = default_tokenizer("  Way     too much     space   here  ")
    assert ["Way", "too", "much", "space", "here"] == list(token_stream)


def test_default_tokenizer_remove_newline():
    token_stream = default_tokenizer("A\nB\n\nC\n\r\nD")
    assert ["A", "B", "C", "D"] == list(token_stream)
