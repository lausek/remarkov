from remarkov.types import TokenStream

PUNCT_TERMINATION = [".", "?", "!"]
PUNCT = [*PUNCT_TERMINATION, ",", "[", "]", "(", ")", ":", '"']


def default_tokenizer(text: str) -> TokenStream:
    text = text.replace("\n", " ").replace("\r", " ")

    for punct in PUNCT:
        text = text.replace(punct, f" {punct} ")

    return (token for token in text.split(" ") if token)
