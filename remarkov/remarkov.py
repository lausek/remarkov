import random

from typing import Callable, Dict, Generator, List, Optional, Tuple

from remarkov.types import State, Token, Tokenizer, TokenStream
from remarkov.tokenizer import (
    NO_WHITESPACE_AFTER,
    default_tokenizer,
    PUNCT,
    PUNCT_TERMINATION,
)


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


class GenerationResult:
    def __init__(self, output_stream: Generator[Token, None, None]):
        self.output_stream = output_stream

    def __str__(self):
        """
        Collects all emitted tokens into a string, putting a space between each token.
        """

        return " ".join(self.output_stream)

    def text(self):
        """
        Collects all emitted tokens and tries to apply correct spacing between punctuation and words.
        """

        from remarkov.tokenizer import NO_WHITESPACE_BEFORE

        prev_token, output = None, ""

        for token in self.output_stream:
            # apply special spacing rules to punctuation.
            if token in NO_WHITESPACE_BEFORE:
                pass
            # make sure that output is not empty to avoid leading whitespace.
            # if we've previously emitted a punctuation token that doesn't require a space -> avoid it.
            elif output and prev_token not in NO_WHITESPACE_AFTER:
                output += " "

            output += token
            prev_token = token

        return output


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

        assert 1 <= self.order, "Order must be greater than 1."

    def _create_initial_state(self, token_stream: TokenStream) -> List[Token]:
        try:
            return [
                self._trigger_before_insert(next(token_stream))
                for _ in range(self.order)
            ]
        except StopIteration:
            raise Exception(
                "Creating an initial chain state exhausted the token stream. "
                "Choose a lower chain order or provide more input text."
            )

    def _get_random_start_state(self) -> Tuple[Tuple[Token], List[Token]]:
        """
        This returns an immutable tuple state for transition selection as first value and
        a mutable variant as second value.
        """
        for _ in range(100):
            # unfortunately, we cannot trust this start state to have a successor token,
            # because the chain could be exhausted if corresponding source text ended.
            key = random.choice(self.transitions.start_states)

            # make sure that the state has successor tokens.
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

            # if we've removed a sentence termination token in the last iteration, we now have a valid start state.
            if last_removed_token in PUNCT_TERMINATION:
                self.transitions.declare_start(key)

            # update current state.
            state.append(token)
            # save the last removed token for starting state detection.
            last_removed_token = state.pop(0)

    def _generate_stream(self, word_amount: int):
        _, state = self._get_random_start_state()

        # copy state tokens into output.
        yield from state

        for _ in range(word_amount):
            key: Tuple[Token] = tuple(state)

            if key not in self.transitions:
                key, state = self._get_random_start_state()

                yield from state

            token = random.choice(self.transitions[key])

            # update state.
            state.append(token)
            state.pop(0)

            yield token

    def generate(self, word_amount: int) -> GenerationResult:
        return GenerationResult(self._generate_stream(word_amount))
