import random

from typing import Callable, Dict, List, Optional, Tuple

from remarkov.types import MarkovChainWalk, State, Token, Tokenizer, TokenStream
from remarkov.tokenizer import default_tokenizer, PUNCT_TERMINATION


def token_to_lowercase(token: str) -> str:
    return token.lower()


class Transitions(dict):
    def __init__(self):
        self.__dict__: Dict[State, List[Token]] = {}
        self.start_states: List[State] = []

    def declare_start(self, from_: State):
        self.start_states.append(from_)

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

    def _get_random_start_state(self) -> Tuple[Tuple[Token], List[Token]]:
        """
        This returns an immutable tuple state for transition selection as first value and
        a mutable variant as second value.
        """
        for _ in range(100):
            # unfortunately, we cannot trust this start state to have a successor token,
            # because the chain could be exhausted if corresponding source text ended.
            key = random.choice(self.transitions.start_states)

            # make sure that the state has successor tokens
            if key in self.transitions:
                break

        else:
            # if we haven't managed to find a start state -> give up.
            raise Exception("Couldn't select a valid start state.")

        return key, list(key)

    def _trigger_before_insert(self, token: str) -> str:
        if self.before_insert:
            return self.before_insert(token)

        return token

    def add_text(self, text: str, tokenizer: Optional[Tokenizer] = None):
        if tokenizer is None:
            tokenizer = self.tokenizer

        token_stream = tokenizer(text)

        last_removed_token, state = None, self._create_initial_state(token_stream)

        for token in token_stream:
            key: Tuple[Token] = tuple(state)

            token = self._trigger_before_insert(token)
            self.transitions.declare(key, token)

            # if we removed a sentence termination token in the last iteration
            # we now have a valid start state.
            if last_removed_token in PUNCT_TERMINATION:
                self.transitions.declare_start(key)

            # update current state
            state.append(token)
            # save the last removed token for starting state detection
            last_removed_token = state.pop(0)

    def generate_text(self, word_amount: int) -> MarkovChainWalk:
        _, state = self._get_random_start_state()

        # copy state tokens into output
        yield from state

        for _ in range(word_amount):
            key: Tuple[Token] = tuple(state)

            if key not in self.transitions:
                key, state = self._get_random_start_state()

                yield from state

            token = random.choice(self.transitions[key])

            # update state
            state.append(token)
            state.pop(0)

            yield token
