from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from stam import AnnotationStore

from pecha_framework.ids import get_base_id, get_initial_pecha_id, get_uuid


class Pecha:
    def __init__(
        self,
        pecha_id: str,
        pecha_path: Path,
        bases: defaultdict = None,
        layers: defaultdict = None,
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
