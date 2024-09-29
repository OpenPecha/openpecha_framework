from pathlib import Path

from pecha_framework.pecha import Pecha


def test_load_doc_from_stam():
    data = Path(__file__).parent / "data"
    pecha_path = data / "I541B3123"

    pecha = Pecha.from_path(pecha_path)
    assert isinstance(pecha, Pecha)


test_load_doc_from_stam()
