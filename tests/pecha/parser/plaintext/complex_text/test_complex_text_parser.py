from pathlib import Path
from shutil import rmtree

from pecha_framework import Document, Pipeline
from pecha_framework.pecha.parser.plain_text.complex_text import (  # noqa
    ComplexTextParser,
)
from pecha_framework.stam_pipe import StamPipe  # noqa


def test_complex_text_parser():
    data_path = Path(__file__).parent / "data"
    text = data_path.joinpath("complex_text.txt").read_text(encoding="utf-8")
    doc = Document(text=text)

    output_path = Path(__file__).parent / "output"
    component_kwargs = {"stam_pipe": {"output_path": output_path}}
    component_names = ["complex_text_parser", "stam_pipe"]

    pipeline = Pipeline(components=component_names, **component_kwargs)
    doc = pipeline(doc)

    pecha = getattr(doc, "pecha")

    # Check if sapche annotations
    sapche_ann_stores = []
    for _, anns in pecha.layers.items():
        for ann_name, ann_store in anns.items():
            if ann_name == "sapche":
                sapche_ann_stores.append(ann_store)
    assert len(sapche_ann_stores) == 1

    sapches = [str(ann) for ann in sapche_ann_stores[0]]
    assert sapches == ["སེ་ཕེ།1", "སེ་ཕེ།2"]

    # Check if sentence annotations
    sentence_ann_stores = []
    for _, anns in pecha.layers.items():
        for ann_name, ann_store in anns.items():
            if ann_name == "sentence":
                sentence_ann_stores.append(ann_store)
    assert len(sentence_ann_stores) == 1

    sentences = [str(ann) for ann in sentence_ann_stores[0]]
    assert sentences == [
        "ཚིག་དང་པོ་ནི།",
        "ཚིག་གཉིས་པ་ནི།",
        "ཚིག་གསུམ་པ་ནི།",
        "ཚིག་གསུམ་པ་ནི།",
    ]

    # clean up
    rmtree(output_path)


test_complex_text_parser()
