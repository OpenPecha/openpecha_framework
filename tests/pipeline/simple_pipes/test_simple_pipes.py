from pathlib import Path

from pecha_framework import Document, Pipe, Pipeline


class SpaceNormalizer(Pipe):
    name = "space_normalizer"

    def __call__(self, doc: Document):
        """Normalize space at start or end of sentence in the document."""
        doc.text = "\n".join(line.strip() for line in doc.text.split("\n"))
        return doc


class Stanza(Pipe):
    name = "stanza_extractor"

    def __call__(self, doc: Document):
        """
        Extract Stanza from the doc.text by two newlines.
        """
        char_count = 0
        stanza_anns = []
        for stanza in doc.text.split("\n\n"):
            stanza_anns.append({"start": char_count, "end": char_count + len(stanza)})
            char_count += len(stanza) + 2
        doc.annotations["stanza"] = stanza_anns
        return doc


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

    """ Test the text attribute """

    stanza_anns = doc.annotations["stanza"]
    assert len(stanza_anns) == 2
    assert stanza_anns == [{"start": 0, "end": 150}, {"start": 152, "end": 295}]

    for stanza_ann, expected_stanza_output in zip(stanza_anns, expected_stanzas_output):
        assert (
            doc.text[stanza_ann["start"] : stanza_ann["end"]]  # noqa
            == expected_stanza_output
        )


test_simple_pipes()
