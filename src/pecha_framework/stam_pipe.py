from pathlib import Path
from typing import List, Tuple

from stam import AnnotationStore, Offset, Selector

from pecha_framework import Document, Pipe
from pecha_framework.ids import get_uuid
from pecha_framework.pecha import Pecha


class StamWriter(Pipe):
    name = "stam_writer"

    def __init__(self, output_path: Path, same_pecha: bool = True):
        self.output_path = output_path
        self.same_pecha = same_pecha
        self.components = {
            "create_pecha": CreatePecha(output_path=self.output_path),
            "create_base_text": CreateBaseText(output_path=self.output_path),
            "create_stam_annotation_file": CreateStamAnnotationFile(
                output_path=self.output_path
            ),
        }

    def __call__(self, doc: Document):
        """
        Write the Document object to STAM format.
        """
        self.output_path.mkdir(parents=True, exist_ok=True)

        formatted_base_ann_mapping = {}
        for base_ann_mapping in doc.base_ann_mapping:
            text_attr, ann_name = base_ann_mapping
            if text_attr not in formatted_base_ann_mapping:
                formatted_base_ann_mapping[text_attr] = [ann_name]
            else:
                formatted_base_ann_mapping[text_attr].append(ann_name)

        if self.same_pecha:
            doc = self.components["create_pecha"](doc)  # type: ignore
            for text_attr, ann_names in formatted_base_ann_mapping.items():
                doc, base_name = self.components["create_base_text"](doc, doc.get_attr(text_attr))  # type: ignore
                for ann_name in ann_names:
                    doc = self.components["create_stam_annotation_file"](
                        doc,  # type: ignore
                        base_name,
                        ann_name,
                        doc.annotations[ann_name],
                    )

        return doc


class CreatePecha(Pipe):
    name = "create_pecha"

    def __init__(self, output_path: Path):
        self.output_path = output_path

    def __call__(self, doc: Document):
        """
        Create a pecha from the Document object.
        """
        pecha = Pecha.create_pecha(self.output_path)
        setattr(doc, "pecha", pecha)
        return doc


class CreateBaseText(Pipe):
    name = "create_base_text"
    requires = ["create_pecha"]

    def __init__(self, output_path: Path):
        self.output_path = output_path

    def __call__(self, doc: Document, base_text: str):
        """
        Create a base text from the Document object.
        """
        pecha = getattr(doc, "pecha")
        base_name = pecha.set_base(base_text)
        return doc, base_name


class CreateStamAnnotationFile(Pipe):
    name = "create_stam_annotation_file"

    def __init__(self, output_path: Path):
        self.output_path = output_path

    def __call__(
        self, doc: Document, base_name: str, ann_name: str, annotations: List[Tuple]
    ):
        """
        Create a stam annotation file from the Document object.
        """
        pecha = getattr(doc, "pecha")
        # Create AnnotationStore object which stores the annotations
        ann_store = AnnotationStore(id=pecha.pecha_id)

        # Set the ann file path
        ann_store_path = pecha.layer_path / base_name / f"{ann_name}.json"
        ann_store_path.parent.mkdir(parents=True, exist_ok=True)
        ann_store.set_filename(str(ann_store_path))

        # Map the base text to the annotation with relative path
        ann_resource = ann_store.add_resource(
            id=f"{base_name}.txt", filename=(f"../../base/{base_name}.txt")
        )
        ann_dataset = ann_store.add_dataset(id="Dataset")

        # Annotate
        for start, end in annotations:
            selector = Selector.textselector(ann_resource, Offset.simple(start, end))
            data = [
                {
                    "id": get_uuid(),
                    "set": ann_dataset.id(),
                    "key": "StructureType",
                    "value": ann_name,
                }
            ]
            ann_store.annotate(id=get_uuid(), target=selector, data=data)

        ann_store.save()
