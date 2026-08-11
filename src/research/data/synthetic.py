"""Deterministic synthetic regression data for smoke tests and examples."""

from __future__ import annotations

import torch
from torch.utils.data import DataLoader, TensorDataset


class SyntheticRegressionData:
    def __init__(
        self,
        dataset_id: str,
        num_train: int,
        num_test: int,
        input_dim: int,
        noise: float,
        batch_size: int,
        seed: int,
    ) -> None:
        self.dataset_id = dataset_id
        self.batch_size = batch_size
        generator = torch.Generator().manual_seed(seed)
        weights = torch.arange(1, input_dim + 1, dtype=torch.float32).unsqueeze(1)
        features = torch.randn(num_train + num_test, input_dim, generator=generator)
        epsilon = noise * torch.randn(num_train + num_test, 1, generator=generator)
        targets = features @ weights + epsilon
        self.train_dataset = TensorDataset(features[:num_train], targets[:num_train])
        self.test_dataset = TensorDataset(features[num_train:], targets[num_train:])

    def train_loader(self) -> DataLoader:
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def test_loader(self) -> DataLoader:
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False)
