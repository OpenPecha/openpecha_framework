import re

from pecha_framework import Document, Pipe


class ComplexTextParser(Pipe):
    name = "complex_text_parser"

    def __init__(self):
        self.components = [SapcheExtractor(), SentenceExtractor()]

    def __call__(self, doc: Document):
        for component in self.components:
            doc = component(doc)  # type: ignore
        return doc


class SapcheExtractor(Pipe):
    name = "sapche_extractor"

    def __call__(self, doc: Document):
        sapche_pattern = r"<sapche>(.*?)<\/sapche>"
        matches = re.finditer(sapche_pattern, doc.text)

        sapche_anns = []
        # Store the spans to avoid for subsequent components
        doc.spans_to_avoid = []
        for match in matches:
            sapche_text_and_ann_span = match.span()
            sapche_text_span = match.span(1)
            sapche_anns.append(sapche_text_span)
            doc.spans_to_avoid.append(sapche_text_and_ann_span)

        doc.annotations["sapche"] = sapche_anns
        doc.base_ann_mapping.append(("text", "sapche"))
        return doc


class SentenceExtractor(Pipe):
    name = "sentence_extractor"
    requires = ["sapche_extractor"]

    def __call__(self, doc: Document):
        splited_text = re.split(r"[\s\n]+", doc.text)
        splited_text = re.findall(r"\S+|\s+", doc.text)

        char_count = 0

        sentence_anns = []
        for text in splited_text:
            if not text.strip():
                char_count += len(text)
                continue
            text_span = (char_count, char_count + len(text))
            avoid_span = False
            for span_to_avoid in doc.spans_to_avoid:
                if (
                    span_to_avoid[0] <= text_span[0]
                    and span_to_avoid[1] >= text_span[1]
                ):
                    avoid_span = True
                    break
            if not avoid_span:
                sentence_anns.append(text_span)
            char_count += len(text)

        doc.annotations["sentence"] = sentence_anns
        doc.base_ann_mapping.append(("text", "sentence"))
        return doc
