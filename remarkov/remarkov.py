from typing import Callable, Dict, List, Optional

from remarkov.types import State, Token, Tokenizer, TokenStream
from remarkov.tokenizer import default_tokenizer


def token_to_lowercase(token: str) -> str:
    return token.lower()


class Transitions(dict):
    def __init__(self):
        self.__dict__: Dict[State, List[Token]] = {}

    def declare(self, from_: State, to: Token):
        if from_ not in self:
            self[from_] = []

        self[from_].append(to)


class ReMarkov:
    def __init__(
        self,
        order: int = 1,
        tokenizer: Tokenizer = default_tokenizer,
        before_insert: Optional[Callable[[str], str]] = token_to_lowercase,
    ):
        self.order = order
        self.tokenizer = tokenizer
        self.before_insert = before_insert

        self.transitions = Transitions()

    def _create_initial_state(self, token_stream: TokenStream) -> List[Token]:
        return [
            self._trigger_before_insert(next(token_stream)) for _ in range(self.order)
        ]

    def _trigger_before_insert(self, token: str) -> str:
        if self.before_insert:
            return self.before_insert(token)

        return token

    def add_text(self, text: str, tokenizer: Optional[Tokenizer] = None):
        if tokenizer is None:
            tokenizer = self.tokenizer

        token_stream = tokenizer(text)

        state = self._create_initial_state(token_stream)

        for token in token_stream:
            key = tuple(state)

            if key not in self.transitions:
                self.transitions[key] = []

            token = self._trigger_before_insert(token)
            self.transitions.declare(key, token)

            # update current state
            state.append(token)
            state.pop(0)
