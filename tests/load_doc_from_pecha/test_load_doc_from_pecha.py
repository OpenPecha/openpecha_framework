from pathlib import Path

from pecha_framework import Document
from pecha_framework.pecha import Pecha


def test_load_doc_from_pecha():
    data = Path(__file__).parent / "data"
    pecha_path = data / "I541B3123"

    pecha = Pecha.from_path(pecha_path)
    assert isinstance(pecha, Pecha)

    doc = Document.from_pecha(pecha=pecha)
    assert isinstance(doc, Document)

    doc_pecha = getattr(doc, "pecha")
    assert isinstance(doc_pecha, Pecha)
    assert doc_pecha == pecha


test_load_doc_from_pecha()
