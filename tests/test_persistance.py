import json
import tempfile
from remarkov import create_model, load_model, parse_model


def test_persist_version_one():
    model = create_model()
    model.add_text("a a a a")
    loaded_model = json.loads(model.to_json(version=1))

    assert 3 == len(loaded_model["transitions"][0]["tokens"])


def test_load_version_one():
    model = create_model()
    model.add_text("a a a a")
    loaded_model = parse_model(model.to_json(version=1), version=1)

    assert model.transitions == loaded_model.transitions
    assert model.transitions.start_states == loaded_model.transitions.start_states


def test_load_version_one_from_file():
    model = create_model()
    model.add_text("a a a a")

    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        tmp.write(model.to_json(version=1))
        tmp.seek(0)

        loaded_model = load_model(tmp.name, version=1)
        assert model.transitions == loaded_model.transitions
        assert model.transitions.start_states == loaded_model.transitions.start_states


def test_default_json_serialization():
    model = create_model()
    model.add_text(
        "This is a sample and this is another. Be sure to have multiple. Sentences."
    )

    assert json.loads(model.to_json())


def test_default_json_persistance():
    model = create_model(order=2)
    model.add_text(
        "This is a sample and this is another. Be sure to have multiple. Sentences."
    )

    source_model = model.to_json()
    loaded_model = parse_model(source_model)

    print(model.transitions.start_states)

    assert 2 == loaded_model.order
    assert loaded_model.transitions
    assert 2 == len(loaded_model.transitions.start_states)
