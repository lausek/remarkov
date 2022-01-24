from typing import Callable
from remarkov.types import TokenStream

PUNCT_TERMINATION = [".", "?", "!"]
"""Punctuation characters that terminate a sentence."""
PUNCT = [*PUNCT_TERMINATION, ",", ":", '"', "[", "]", "(", ")"]
"""All special characters that should be tokenized."""

NO_WHITESPACE_BEFORE = [*PUNCT_TERMINATION, ",", ":", ")", "]"]
NO_WHITESPACE_AFTER = ["[", "("]


def default_tokenizer(text: str) -> TokenStream:
    """
    Simple tokenizer that splits a sentence and creates a token for each word or punctuation character.
    """

    text = text.replace("\n", " ").replace("\r", " ")

    for punct in PUNCT:
        text = text.replace(punct, f" {punct} ")

    return (token for token in text.split(" ") if token)


def token_to_lowercase(token: str) -> str:
    return token.lower()


def token_to_uppercase(token: str) -> str:
    return token.upper()


def create_ngram_tokenizer(n: int) -> Callable[[str], TokenStream]:
    """
    Tokenize the input text into n-grams of length `n`. Short tokens are padded with whitespace.
    """

    assert 0 < n, "n must be at least 1"

    def ngram_tokenizer(text: str):
        for offset in range(0, len(text), n):
            ngram = text[offset : offset + n]
            ngram_len_diff = n - len(ngram)

            # if the current ngram is too short, pad it with whitespace.
            if 0 < ngram_len_diff:
                ngram += " " * ngram_len_diff

            yield ngram

    return ngram_tokenizer
