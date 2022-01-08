from typing import Callable, Generator, Tuple

Token = str
TokenStream = Generator[Token, None, None]
Tokenizer = Callable[[str], TokenStream]
State = Tuple[Token]
