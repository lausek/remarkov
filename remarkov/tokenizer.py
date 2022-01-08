from remarkov.types import TokenStream


def default_tokenizer(text: str) -> TokenStream:
    for punct in [".", ",", "?", "!", "[", "]", "(", ")"]:
        text = text.replace(punct, f" {punct} ")

    return (token for token in text.split(" ") if token)
