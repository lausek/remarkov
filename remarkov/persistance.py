from json import JSONDecoder, JSONEncoder

ORDER, TRANSITIONS, START_STATES = "order", "transitions", "start_states"
DEFAULT_JSON_INDENT = 4


class V1Decoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.__object_hook)

    def __object_hook(self, obj):
        if ORDER in obj and TRANSITIONS in obj and START_STATES in obj:
            from remarkov.model import Model

            remarkov = Model()
            remarkov.order = obj[ORDER]

            for transition in obj[TRANSITIONS]:
                state = tuple(transition["state"])
                for token in transition["tokens"]:
                    remarkov.transitions.declare(state, token)

            for start_state in obj[START_STATES]:
                remarkov.transitions.declare_start(tuple(start_state))

            return remarkov

        return obj


class V1Encoder(JSONEncoder):
    def __init__(self, compress: bool):
        super().__init__(indent=None if compress else DEFAULT_JSON_INDENT)

    def default(self, obj):
        return {
            ORDER: obj.order,
            # save each transition as an object
            TRANSITIONS: [
                {"state": list(state), "tokens": tokens}
                for state, tokens in obj.transitions.items()
            ],
            START_STATES: [list(state) for state in obj.transitions.start_states],
        }
