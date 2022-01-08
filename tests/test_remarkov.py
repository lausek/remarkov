from remarkov.prelude import ReMarkov


def test_remarkov_transitions_simple():
    remarkov = ReMarkov()
    remarkov.add_text("I have a dream.")

    for key in ["I", "have", "a", "dream"]:
        assert (key,) in remarkov.transitions

    assert (".",) not in remarkov.transitions
