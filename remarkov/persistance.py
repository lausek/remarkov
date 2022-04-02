from collections import defaultdict
from json import JSONDecoder, JSONEncoder
from typing import Dict, List, Union

from remarkov.types import Token

ORDER, TRANSITIONS, START_STATES = "order", "transitions", "start_states"
DEFAULT_JSON_INDENT = 4
DEFAULT_PERSISTANCE_VERSION = 1


class GenericEncoder(JSONEncoder):
    def __init__(self, compress: bool):
        super().__init__(indent=None if compress else DEFAULT_JSON_INDENT)

    def _adapt_tokens(
        self, tokens: List[Token]
    ) -> Union[Dict[Token, int], List[Token]]:
        raise NotImplementedError()

    def default(self, obj):
        return {
            ORDER: obj.order,
            # save each transition as an object
            TRANSITIONS: [
                {"state": list(state), "tokens": self._adapt_tokens(tokens)}
                for state, tokens in obj.transitions.items()
            ],
            START_STATES: [list(state) for state in obj.transitions.start_states],
        }


class GenericDecoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.__object_hook)

    def _declare_transitions(
        self, model, state, tokens: Union[Dict[Token, int], List[Token]]
    ):
        raise NotImplementedError()

    def __object_hook(self, obj):
        if ORDER in obj and TRANSITIONS in obj and START_STATES in obj:
            from remarkov.model import Model

            remarkov = Model()
            remarkov.order = obj[ORDER]

            for transition in obj[TRANSITIONS]:
                state = tuple(transition["state"])
                self._declare_transitions(remarkov, state, transition["tokens"])

            for start_state in obj[START_STATES]:
                remarkov.transitions.declare_start(tuple(start_state))

            return remarkov

        return obj


class V1Decoder(GenericDecoder):
    def _declare_transitions(
        self, model, state, tokens: Union[Dict[Token, int], List[Token]]
    ):
        for token in tokens:
            model.transitions.declare(state, token)


class V1Encoder(GenericEncoder):
    def _adapt_tokens(
        self, tokens: List[Token]
    ) -> Union[Dict[Token, int], List[Token]]:
        return tokens


class V2Decoder(GenericDecoder):
    def _declare_transitions(
        self, model, state, tokens: Union[Dict[Token, int], List[Token]]
    ):
        for token, count in tokens.items():
            for _ in range(count):
                model.transitions.declare(state, token)


class V2Encoder(GenericEncoder):
    def _adapt_tokens(
        self, tokens: List[Token]
    ) -> Union[Dict[Token, int], List[Token]]:
        count_aggregation = defaultdict(int)
        for token in tokens:
            count_aggregation[token] += 1
        return count_aggregation
