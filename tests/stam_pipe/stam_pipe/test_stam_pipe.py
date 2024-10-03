from pathlib import Path
from shutil import rmtree

from pecha_framework import Document, Pipeline
from pecha_framework.pecha import Pecha
from pecha_framework.stam_pipe import StamPipe  # noqa


def test_stam_pipe():
    doc = Document(
        text="",
        resources={"text": "Hello, world!\nThis is a test."},
        annotations={"lines": [(0, 13), (14, 28)]},
        resource_ann_mapping=[("text", "lines")],
    )

    output_path = Path(__file__).parent / "output"

    component_names = ["stam_pipe"]
    component_kwargs = {"stam_pipe": {"output_path": output_path}}
    pipeline = Pipeline(components=component_names, **component_kwargs)
    doc = pipeline(doc)

    # Check if pecha is created and saved to doc
    assert hasattr(doc, "pecha")
    pecha = getattr(doc, "pecha")
    assert isinstance(pecha, Pecha)

    # Check if line annotation stam file is saved to pecha
    lines_ann_stores = []
    for _, anns in pecha.layers.items():
        for ann_name, ann_store in anns.items():
            if ann_name == "lines":
                lines_ann_stores.append(ann_store)
    assert len(lines_ann_stores) == 1

    # Check if the annotations are saved correctly
    lines = [str(ann) for ann in lines_ann_stores[0]]
    assert lines == ["Hello, world!", "This is a test"]

    # Clean up
    rmtree(output_path)


test_stam_pipe()
