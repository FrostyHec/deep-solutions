"""Tests for PyTorch DataLoader parameter selector."""

import pytest

torch = pytest.importorskip("torch")
from torch.utils.data import TensorDataset  # noqa: E402

from deep_solutions.parameter_search.pytorch.dataloader import (  # noqa: E402
    DataLoaderParamSelector,
)


class TestDataLoaderParamSelector:
    """Test DataLoaderParamSelector end-to-end."""

    @staticmethod
    def _make_dataset(n_samples: int = 500) -> TensorDataset:
        """Create a simple TensorDataset for testing."""
        x = torch.randn(n_samples, 10)
        y = torch.randint(0, 5, (n_samples,))
        return TensorDataset(x, y)

    def test_finds_best_config(self) -> None:
        """Should return best_config with valid throughput."""
        dataset = self._make_dataset()
        selector = DataLoaderParamSelector(
            dataset=dataset,
            search_space={
                "batch_size": [16, 32],
                "num_workers": [0],
            },
            repeats=1,
            batches_per_run=5,
        )
        output = selector.run()

        assert "best_config" in output
        assert "best_throughput" in output
        assert output["best_config"] is not None
        assert output["best_throughput"] > 0
        assert "batch_size" in output["best_config"]

    def test_with_chart(self, tmp_path) -> None:
        """Should generate chart when chart_path is provided."""
        dataset = self._make_dataset()
        chart_path = str(tmp_path / "test_chart.png")

        selector = DataLoaderParamSelector(
            dataset=dataset,
            search_space={
                "batch_size": [16, 32],
                "num_workers": [0],
            },
            repeats=1,
            batches_per_run=5,
            chart_path=chart_path,
        )
        output = selector.run()

        assert "chart" in output
        assert output["chart"]["chart_path"] == chart_path

    def test_fixed_params(self) -> None:
        """Fixed params like pin_memory should be passed through."""
        dataset = self._make_dataset()
        selector = DataLoaderParamSelector(
            dataset=dataset,
            search_space={"batch_size": [32]},
            fixed_params={"num_workers": 0, "pin_memory": False},
            repeats=1,
            batches_per_run=3,
        )
        output = selector.run()

        assert output["best_config"] is not None

    def test_search_result_accessible(self) -> None:
        """search_result should be accessible for advanced usage."""
        dataset = self._make_dataset()
        selector = DataLoaderParamSelector(
            dataset=dataset,
            search_space={"batch_size": [16, 64]},
            fixed_params={"num_workers": 0},
            repeats=1,
            batches_per_run=3,
        )
        output = selector.run()

        sr = output["search_result"]
        assert len(sr) == 2
        assert len(sr.records) == 2
