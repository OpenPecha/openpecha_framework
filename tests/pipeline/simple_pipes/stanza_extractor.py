from pecha_framework.pipeline import Document, Pipe


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
