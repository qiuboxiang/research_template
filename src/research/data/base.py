"""Data module protocol."""

from __future__ import annotations

from typing import Any, Protocol


class DataModule(Protocol):
    dataset_id: str

    def train_loader(self) -> Any: ...

    def test_loader(self) -> Any: ...
