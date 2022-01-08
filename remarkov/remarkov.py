from typing import Callable, Dict, List, Optional

from remarkov.types import State, Token, Tokenizer, TokenStream
from remarkov.tokenizer import default_tokenizer


def token_to_lowercase(token: str) -> str:
    return token.lower()


class ReMarkov:
    def __init__(
        self,
        order: int,
        tokenizer: Tokenizer = default_tokenizer,
        before_insert: Optional[Callable[[str], str]] = token_to_lowercase,
    ):
        self.order = order
        self.tokenizer = tokenizer
        self.before_insert = before_insert

        self.transitions: Dict[State, Token] = {}

    def _create_initial_state(self, token_stream: TokenStream) -> List[Token]:
        return [next(token_stream) for _ in range(self.order)]

    def add_text(self, text: str, tokenizer: Optional[Tokenizer] = None):
        if tokenizer is None:
            tokenizer = self.tokenizer

        token_stream = tokenizer(text)

        state = self._create_initial_state(token_stream)

        for token in token_stream:
            pass
