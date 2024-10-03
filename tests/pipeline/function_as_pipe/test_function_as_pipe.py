import re

from pecha_framework import Document, Pipeline, pipe_component


@pipe_component(name="filter_tibetan_words", requires=[])
def filter_tibetan_words(doc: Document):
    """
    Filter Tibetan words from the doc.text
    """
    doc.filtered_text = "".join(re.findall(r"[\u0F00-\u0FFF]+", doc.text))
    return doc


@pipe_component(name="tibetan_word_extractor", requires=[])
def tibetan_word_extractor(doc: Document):
    """
    Extract Tibetan words from the doc.filtered_text with tsek and shad
    """
    assert hasattr(
        doc, "filtered_text"
    ), "filtered_text attribute is missing in the doc object"

    last_offset = 0
    word_anns = []
    for i, char in enumerate(doc.filtered_text):
        if char in ["་", "།"]:
            word_anns.append({"start": last_offset, "end": i + 1})
            last_offset = i + 1

    doc.annotations["tibetan_words"] = word_anns
    return doc


expected_bo_words = [
    "ང་",
    "སྨོན་",
    "ལམ་",
    "ཨ་",
    "ཡེ་",
    "ལ་",
    "ལས་",
    "ཀ་",
    "བྱེད་",
    "ཀྱི་",
    "ཡོད།",
]


def test_function_as_pipes():
    text = "ང་སྨོན་ལམ་ཨ་ཡེ་(Monlam AI)ལ་ལས་ཀ་བྱེད་ཀྱི་ཡོད།"
    doc = Document(text=text)
    pipeline = Pipeline(components=["filter_tibetan_words", "tibetan_word_extractor"])
    doc = pipeline(doc)

    """ Test the filtered_text attribute """
    assert doc.filtered_text == "ང་སྨོན་ལམ་ཨ་ཡེ་ལ་ལས་ཀ་བྱེད་ཀྱི་ཡོད།"

    bo_word_anns = doc.annotations["tibetan_words"]
    assert len(bo_word_anns) == 11
    for bo_word_ann, expected_bo_word in zip(bo_word_anns, expected_bo_words):
        assert (
            doc.filtered_text[bo_word_ann["start"] : bo_word_ann["end"]]  # noqa
            == expected_bo_word
        )


test_function_as_pipes()
