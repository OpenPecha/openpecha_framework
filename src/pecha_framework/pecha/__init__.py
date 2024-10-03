from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Optional

from stam import AnnotationStore

from pecha_framework.ids import get_base_id, get_initial_pecha_id, get_uuid


class Pecha:
    def __init__(
        self,
        pecha_id: str,
        pecha_path: Path,
        bases: Optional[DefaultDict[str, str]] = None,
        layers: Optional[DefaultDict[str, DefaultDict[str, AnnotationStore]]] = None,
    ):
        self.pecha_id = pecha_id
        self.pecha_path = pecha_path
        self.bases = bases if bases else defaultdict(str)
        self.layers = layers if layers else defaultdict(lambda: defaultdict(str))

    @classmethod
    def create_pecha(cls, path: Path):
        pecha_id = get_initial_pecha_id()
        pecha_path = path / pecha_id
        pecha_path.mkdir(parents=True, exist_ok=True)
        return cls(pecha_id, pecha_path)

    @classmethod
    def from_path(cls, pecha_path: Path):
        pecha_id = pecha_path.name

        # load base files
        base_files = list(pecha_path.joinpath("base").rglob("*.txt"))
        bases = defaultdict(
            str,
            {
                base_file.stem: base_file.read_text(encoding="utf-8")
                for base_file in base_files
            },
        )

        # load layer files
        layers: DefaultDict[str, DefaultDict[str, AnnotationStore]] = defaultdict(
            lambda: defaultdict(str)
        )
        layer_files = list(pecha_path.joinpath("layer").rglob("*.json"))
        for layer_file in layer_files:
            base_name = layer_file.parent.name
            ann_name = layer_file.stem.split("-")[0]
            ann_store = AnnotationStore(file=layer_file.as_posix())
            layers[base_name][ann_name] = ann_store

        return cls(pecha_id, pecha_path, bases, layers)

    @property
    def base_path(self):
        base_path = self.pecha_path / "base"
        base_path.mkdir(parents=True, exist_ok=True)
        return base_path

    @property
    def layer_path(self):
        layer_path = self.pecha_path / "layer"
        layer_path.mkdir(parents=True, exist_ok=True)
        return layer_path

    def set_base(self, content: str, name: str = None) -> str:
        name = get_base_id() if not name else name
        self.base_path.joinpath(f"{name}.txt").write_text(content, encoding="utf-8")
        self.bases[name] = content
        return name

    def set_layer(self, base_name: str, ann_name: str, ann_store: AnnotationStore):
        ann_store_path = (
            self.layer_path / base_name / f"{ann_name}-{get_uuid()[:3]}.json"
        )
        ann_store.set_filename(str(ann_store_path))
        ann_store.save()
        self.layers[base_name][ann_name] = ann_store
        return ann_store_path

    @staticmethod
    def get_annotations(ann_store: AnnotationStore):
        anns = []
        for ann in ann_store:
            start = ann.offset().begin().value()
            end = ann.offset().end().value()
            anns.append((start, end))
        return anns
