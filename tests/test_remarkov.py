from remarkov.prelude import ReMarkov


def test_remarkov_before_insert_disabled():
    remarkov = ReMarkov(before_insert=None)
    remarkov.add_text("I have a dream.")

    for key in ["I", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_remarkov_before_insert():
    remarkov = ReMarkov(before_insert=lambda token: token.upper())
    remarkov.add_text("I have a dream.")

    for key in ["I", "HAVE", "A", "DREAM"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_remarkov_transitions_simple():
    remarkov = ReMarkov()
    remarkov.add_text("I HaVe A dReAm.")

    for key in ["i", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_remarkov_transitions_sentences():
    remarkov = ReMarkov()
    remarkov.add_text("And this. This is not me.")
