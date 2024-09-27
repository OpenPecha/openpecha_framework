from pathlib import Path

from pecha_framework.ids import get_base_id, get_initial_pecha_id


class Pecha:
    def __init__(self, pecha_id: str, pecha_path: Path):
        self.pecha_id = pecha_id
        self.pecha_path = pecha_path

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
        return name
