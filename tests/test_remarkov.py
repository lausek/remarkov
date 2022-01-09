from remarkov.prelude import ReMarkov, token_to_lowercase, token_to_uppercase


def test_remarkov_before_insert_disabled():
    remarkov = ReMarkov(before_insert=None)
    remarkov.add_text("I have a dream.")

    for key in ["I", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_remarkov_before_insert():
    remarkov = ReMarkov(before_insert=token_to_uppercase)
    remarkov.add_text("I have a dream.")

    for key in ["I", "HAVE", "A", "DREAM"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_remarkov_transitions_simple():
    remarkov = ReMarkov(before_insert=token_to_lowercase)
    remarkov.add_text("I HaVe A dReAm.")

    for key in ["i", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions


def test_remarkov_works_without_declared_start():
    remarkov = ReMarkov(before_insert=token_to_lowercase)
    remarkov.add_text("Way too simple sentence")
    assert remarkov.generate(5).text()
