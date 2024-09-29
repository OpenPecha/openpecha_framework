from pecha_framework import Document, Pipe, Pipeline


class LineExtractor(Pipe):
    name = "line_extractor"

    def __call__(self, doc: Document):
        """
        Extract the lines from the text and store them in the Document object.
        """
        char_count = 0
        line_anns = []

        for line in doc.text.split("\n"):
            line_anns.append((char_count, char_count + len(line)))
            char_count += len(line) + 1
        doc.annotations["lines"] = line_anns
        doc.base_ann_mapping.append(("text", "lines"))
        return doc


def test_storing_base_ann_mapping():
    doc = Document(text="Hello, world!\nThis is a test.")
    pipeline = Pipeline(["line_extractor"])
    doc = pipeline(doc)
    assert doc.annotations["lines"] == [(0, 13), (14, 29)]
    assert doc.base_ann_mapping == [("text", "lines")]
