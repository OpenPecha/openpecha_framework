from pathlib import Path

from pecha_framework import Document
from pecha_framework.pecha import Pecha


def test_load_doc_from_pecha():
    data = Path(__file__).parent / "data"
    pecha_path = data / "I541B3123"

    # Check if we can load pecha from path
    pecha = Pecha.from_path(pecha_path)
    assert isinstance(pecha, Pecha)

    # Check if we can load doc with pecha
    doc = Document.from_pecha(pecha=pecha)
    assert isinstance(doc, Document)
    del pecha

    # Check if we can access pecha from doc
    doc_pecha = getattr(doc, "pecha")
    assert isinstance(doc_pecha, Pecha)

    # Check if doc values are properly loaded from pecha
    assert doc.annotations == {"lines": [(0, 13), (14, 28)]}
    assert doc.resource_ann_mapping == [("E23B", "lines")]
    assert doc.E23B == "Hello, world!\nThis is a test."


test_load_doc_from_pecha()
