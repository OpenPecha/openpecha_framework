from pathlib import Path

from stanza_extractor import SpaceNormalizer, Stanza  # noqa

from pecha_framework.pipeline import Document, Pipeline

expected_stanzas_output = [
    "The night was still, the moon aglow,\nA silver thread on earth below.\nThe stars, like diamonds, softly gleamed,\nWhile all the world in silence dreamed.",  # noqa
    "The dawn approached with colors bright,\nA palette born from endless night.\nThe sky transformed from dark to gold,\nAs stories of the day unfold.",  # noqa
]


def test_simple_pipes():
    data = Path(__file__).parent / "data"
    english_poem = Path(data / "english_poem.txt").read_text(encoding="utf-8")

    doc = Document(text=english_poem)
    pipeline = Pipeline(components=["space_normalizer", "stanza_extractor"])
    doc = pipeline(doc)

    stanza_anns = doc.annotations["stanza"]
    assert len(stanza_anns) == 2
    assert stanza_anns == [{"start": 0, "end": 150}, {"start": 152, "end": 295}]

    for stanza_ann, expected_stanza_output in zip(stanza_anns, expected_stanzas_output):
        assert (
            doc.text[stanza_ann["start"] : stanza_ann["end"]]  # noqa
            == expected_stanza_output
        )


test_simple_pipes()
