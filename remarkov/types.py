from typing import Callable, Generator, Optional, Tuple

Token = str
TokenStream = Generator[Token, None, None]
Tokenizer = Callable[[str], TokenStream]
State = Tuple[Token]

MarkovChainWalk = Generator[str, None, None]
