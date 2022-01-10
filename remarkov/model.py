import random

from typing import Callable, Dict, Generator, List, Optional, Tuple

from remarkov.error import NoTransitionsDefined, NoStartStateFound, TokenStreamExhausted
from remarkov.persistance import V1Decoder, V1Encoder
from remarkov.types import State, Token, Tokenizer, TokenStream
from remarkov.tokenizer import (
    NO_WHITESPACE_AFTER,
    default_tokenizer,
    PUNCT_TERMINATION,
)

DEFAULT_GENERATE_WORD_AMOUNT = 32


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


class ReMarkovModel:
    def __init__(
        self,
        order: int = 1,
        tokenizer: Tokenizer = default_tokenizer,
        before_insert: Optional[Callable[[str], str]] = None,
    ):
        self.order = order
        self.tokenizer = tokenizer
        self.before_insert = before_insert

        self.transitions = Transitions()

        assert 1 <= self.order, "Order must be greater than 1."

    @classmethod
    def from_json(cls: "ReMarkovModel", raw: str) -> "ReMarkovModel":
        return V1Decoder().decode(raw)

    def _create_initial_state(self, token_stream: TokenStream) -> List[Token]:
        try:
            return [
                self._trigger_before_insert(next(token_stream))
                for _ in range(self.order)
            ]
        except StopIteration:
            raise TokenStreamExhausted()

    def _get_random_start_state(self) -> Tuple[Tuple[Token], List[Token]]:
        """
        This returns an immutable tuple state for transition selection as first value and
        a mutable variant as second value.
        """
        # if there are no transitions, no data was given. fail.
        if not self.transitions:
            raise NoTransitionsDefined()

        # if no start states were declared, it is most likely because too few sentences were
        # imported. just pick some random key then.
        if not self.transitions.start_states:
            # TODO: avoid this list conversion
            key = random.choice(list(self.transitions.keys()))

        else:
            for _ in range(100):
                # unfortunately, we cannot trust this start state to have a successor token,
                # because the chain could be exhausted if corresponding source text ended.
                key = random.choice(self.transitions.start_states)

                # make sure that the state has successor tokens.
                if key in self.transitions:
                    break

            else:
                # if we haven't managed to find a start state -> give up.
                raise NoStartStateFound()

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

            # decide whether we should declare the current state a valid entry point of the chain.
            if (
                # we consider the beginning of a text to be a valid entry point so check if this is the first iteration.
                last_removed_token is None
                # if we've removed a sentence termination token in the last iteration, we now have a valid start state.
                or last_removed_token in PUNCT_TERMINATION
            ):
                self.transitions.declare_start(key)

            # update current state.
            state.append(token)
            # save the last removed token for starting state detection.
            last_removed_token = state.pop(0)

    def _generate_stream(self):
        """
        Creates an endless stream of words.
        """

        _, state = self._get_random_start_state()

        # copy state tokens into output.
        yield from state

        while True:
            key: Tuple[Token] = tuple(state)

            if key not in self.transitions:
                key, state = self._get_random_start_state()

                yield from state

            token = random.choice(self.transitions[key])

            # update state.
            state.append(token)
            state.pop(0)

            yield token

    def _generate_stream_with_limit(self, word_amount: int):
        """
        This encapsulates text output termination.
        """

        stream = self._generate_stream()
        for _ in range(word_amount):
            yield next(stream)

    def generate(
        self, word_amount: int = DEFAULT_GENERATE_WORD_AMOUNT
    ) -> GenerationResult:
        return GenerationResult(self._generate_stream_with_limit(word_amount))

    def to_json(self, version=1, compress: bool = False) -> str:
        return V1Encoder(compress=compress).encode(self)
