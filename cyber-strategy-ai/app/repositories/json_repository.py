import json
from pathlib import Path
from typing import Any


class JsonRepository:
    """Simple JSON-file-backed list store."""

    def __init__(self, filepath: str) -> None:
        self.path = Path(filepath)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]")

    def _load(self) -> list[dict]:
        text = self.path.read_text()
        return json.loads(text) if text.strip() else []

    def _save(self, data: list[dict]) -> None:
        self.path.write_text(json.dumps(data, indent=2, default=str))

    def all(self) -> list[dict]:
        return self._load()

    def get(self, id_field: str, id_value: str) -> dict | None:
        for item in self._load():
            if item.get(id_field) == id_value:
                return item
        return None

    def insert(self, record: dict) -> dict:
        data = self._load()
        data.append(record)
        self._save(data)
        return record

    def update(self, id_field: str, id_value: str, updates: dict) -> dict | None:
        data = self._load()
        for item in data:
            if item.get(id_field) == id_value:
                item.update(updates)
                self._save(data)
                return item
        return None
