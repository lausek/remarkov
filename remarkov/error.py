class NoTransitionsDefined(Exception):
    def __init__(self):
        super().__init__(
            "The Markov chain does not have any transitions. "
            "This is probably due to invalid operation i.e. generate was called before text was added."
        )


class NoStartStateFound(Exception):
    def __init__(self):
        super().__init__("Couldn't select a valid start state.")


class TokenStreamExhausted(Exception):
    def __init__(self):
        super().__init__(
            "Creating an initial chain state exhausted the token stream. "
            "Choose a lower chain order or provide more input text."
        )
