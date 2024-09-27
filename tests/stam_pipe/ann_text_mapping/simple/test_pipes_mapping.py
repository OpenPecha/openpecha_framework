from pecha_framework.pipeline import Document, Pipe, Pipeline


class FilterText(Pipe):
    name = "filter_text"

    def __call__(self, doc: Document):
        """
        Filter the text into english and tibetan text and store them in the Document object.
        """
        english_lines, tibetan_lines = [], []
        for line in doc.text.split("\n"):
            if line.isascii():
                english_lines.append(line)
            else:
                tibetan_lines.append(line)

        setattr(doc, "english_text", " ".join(english_lines))
        setattr(doc, "tibetan_text", " ".join(tibetan_lines))
        return doc


class EnglishWordExtractor(Pipe):
    name = "english_word_extractor"
    requires = ["filter_text"]

    def __call__(self, doc: Document):
        """
        Extract the english words from the doc.english_text and store them in the Document object.
        """
        char_count = 0
        word_anns = []
        for word in getattr(doc, "english_text").split():
            word_anns.append((char_count, char_count + len(word)))
            char_count += len(word) + 1
        doc.annotations["english_words"] = word_anns
        doc.base_ann_mapping.append(("english_text", "english_words"))
        return doc


def test_storing_base_ann_mapping():
    doc = Document(text="Hello world\nའཇིག་རྟེན་ཁམས་བདེ་ལེགས།")
    pipeline = Pipeline(["filter_text", "english_word_extractor"])
    doc = pipeline(doc)

    assert hasattr(doc, "english_text")
    assert getattr(doc, "english_text") == "Hello world"
    en_word_anns = doc.annotations["english_words"]
    assert en_word_anns == [(0, 5), (6, 11)]
    assert doc.base_ann_mapping == [("english_text", "english_words")]

    expected_en_words = ["Hello", "world"]
    for ann, expected_en_word in zip(en_word_anns, expected_en_words):
        assert getattr(doc, "english_text")[ann[0] : ann[1]] == expected_en_word  # noqa


test_storing_base_ann_mapping()
