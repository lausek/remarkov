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
