from pathlib import Path

from pecha_framework import Document, Pipeline
from pecha_framework.stam_pipe import StamPipe  # noqa


def test_stam_pipe():
    doc = Document(
        text="Hello, world!\nThis is a test.",
        annotations={"lines": [(0, 13), (14, 28)]},
        base_ann_mapping=[("text", "lines")],
    )

    output_path = Path(__file__).parent / "output"

    component_names = ["stam_pipe"]
    component_kwargs = {"stam_pipe": {"output_path": output_path}}
    pipeline = Pipeline(components=component_names, **component_kwargs)
    doc = pipeline(doc)


test_stam_pipe()
