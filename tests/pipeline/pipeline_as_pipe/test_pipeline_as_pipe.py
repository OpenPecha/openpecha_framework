from pecha_framework.pipeline import Document, Pipe, Pipeline


class PlainTextParser(Pipe):
    name = "plain_text_parser"

    def __init__(self):
        self.components = [SentenceExtractor(), WordExtractor()]

    def __call__(self, doc):
        """Process the document through the composite pipe's components."""
        for component in self.components:
            doc = component(doc)  # type: ignore
        return doc


class SentenceExtractor(Pipe):
    name = "sentence_extractor"

    def __call__(self, doc: Document):
        char_count = 0
        sentence_anns = []
        for line in doc.text.split("\n"):
            if line:
                sentence_anns.append(
                    {"start": char_count, "end": char_count + len(line)}
                )
                char_count += len(line) + 1
        doc.annotations["sentence"] = sentence_anns
        return doc


class WordExtractor(Pipe):
    name = "word_extractor"
    requires = ["sentence_extractor"]

    def __call__(self, doc: Document):
        word_anns = []
        for sentence_ann in doc.annotations["sentence"]:
            text = doc.text[sentence_ann["start"] : sentence_ann["end"]]  # noqa
            words = text.split(" ")
            char_count = sentence_ann["start"]
            for word in words:
                word_anns.append({"start": char_count, "end": char_count + len(word)})
                char_count += len(word) + 1
        doc.annotations["words"] = word_anns
        return doc


def test_pipeline_as_pipe():
    english_poem = (
        "The night was still, the moon aglow,\nA silver thread on earth below."
    )

    doc = Document(text=english_poem)
    pipeline = Pipeline(components=["plain_text_parser"])
    doc = pipeline(doc)

    """ Test the result  """

    sentence_anns = doc.annotations["sentence"]
    assert len(sentence_anns) == 2
    assert (
        doc.text[sentence_anns[0]["start"] : sentence_anns[0]["end"]]  # noqa
        == "The night was still, the moon aglow,"
    )
    assert (
        doc.text[sentence_anns[1]["start"] : sentence_anns[1]["end"]]  # noqa
        == "A silver thread on earth below."
    )

    word_anns = doc.annotations["words"]
    assert len(word_anns) == 13
    assert doc.text[word_anns[0]["start"] : word_anns[0]["end"]] == "The"  # noqa
    assert doc.text[word_anns[1]["start"] : word_anns[1]["end"]] == "night"  # noqa


test_pipeline_as_pipe()
