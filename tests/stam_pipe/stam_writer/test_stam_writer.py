from pathlib import Path

from pecha_framework.pipeline import Document, Pipeline
from pecha_framework.stam_pipe import StamWriter  # noqa


def test_stam_writer():
    doc = Document(
        text="Hello, world!\nThis is a test.",
        annotations={"lines": [(0, 13), (14, 29)]},
        ann_text_mapping=[("text", "lines")],
    )

    output_path = Path(__file__).parent / "output"

    component_names = ["stam_writer"]
    component_kwargs = {"stam_writer": {"output_path": output_path}}
    pipeline = Pipeline(components=component_names, **component_kwargs)
    doc = pipeline(doc)


test_stam_writer()
