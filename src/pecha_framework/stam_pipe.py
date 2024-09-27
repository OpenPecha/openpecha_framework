from pathlib import Path

from pecha_framework.pecha import Pecha
from pecha_framework.pipeline import Document, Pipe


class StamWriter(Pipe):
    name = "stam_writer"

    def __init__(self, output_path: Path, same_pecha: bool = True):
        self.components = {
            "create_pecha": CreatePecha(),
            "create_base_text": CreateBaseText(),
        }
        self.output_path = output_path
        self.same_pecha = same_pecha

    def __call__(self, doc: Document):
        """
        Write the Document object to STAM format.
        """
        self.output_path.mkdir(parents=True, exist_ok=True)
        setattr(doc, "output_path", self.output_path)

        base_ann_mapping = {}
        for ann_text_mapping in doc.ann_text_mapping:
            text_attr, ann_name = ann_text_mapping
            if text_attr not in base_ann_mapping:
                base_ann_mapping[text_attr] = [ann_name]
            else:
                base_ann_mapping[text_attr].append(ann_name)

        if self.same_pecha:
            doc = self.components["create_pecha"](doc)  # type: ignore
            for text_attr, _ in base_ann_mapping.items():
                doc = self.components["create_base_text"](doc, doc.get_attr(text_attr))  # type: ignore

        return doc


class CreatePecha(Pipe):
    name = "create_pecha"

    def __call__(self, doc: Document):
        """
        Create a pecha from the Document object.
        """
        pecha = Pecha.create_pecha(getattr(doc, "output_path"))
        setattr(doc, "pecha", pecha)
        return doc


class CreateBaseText(Pipe):
    name = "create_base_text"
    requires = ["create_pecha"]

    def __call__(self, doc: Document, base_text: str):
        """
        Create a base text from the Document object.
        """
        pecha = getattr(doc, "pecha")
        pecha.set_base(base_text)
        return doc
