"""Tests for epoch implementations and analyzers."""

import os
import tempfile

from deep_solutions.parameter_search.analyzers.best_param import (
    BestParamAnalyzer,
)
from deep_solutions.parameter_search.analyzers.chart import ChartAnalyzer
from deep_solutions.parameter_search.core.searcher import ParamSearcher
from deep_solutions.parameter_search.epochs.basic import (
    simple_epoch,
    timed_epoch,
)


class TestTimedEpoch:
    """Test timed_epoch factory function."""

    def test_measures_throughput(self) -> None:
        """timed_epoch should return throughput metrics."""

        def run_func(config, init_result):
            return 100  # processed 100 samples

        epoch_fn = timed_epoch(run_func, repeats=2)
        metrics = epoch_fn({"batch_size": 32}, None)

        assert "throughput" in metrics
        assert "mean_time" in metrics
        assert "total_time" in metrics
        assert metrics["throughput"] > 0

    def test_invalid_repeats_raises(self) -> None:
        """repeats < 1 should raise ValueError."""
        import pytest

        with pytest.raises(ValueError):
            timed_epoch(lambda c, r: 0, repeats=0)


class TestSimpleEpoch:
    """Test simple_epoch wrapper."""

    def test_passthrough(self) -> None:
        """simple_epoch should pass through the eval function."""

        def eval_fn(config, init_result):
            return {"custom": config["x"] * 2.0}

        epoch_fn = simple_epoch(eval_fn)
        metrics = epoch_fn({"x": 5}, None)
        assert metrics == {"custom": 10.0}


class TestBestParamAnalyzer:
    """Test BestParamAnalyzer."""

    def _make_result(self):
        """Helper: create a SearchResult with known data."""
        searcher = ParamSearcher(
            init_func=lambda c: None,
            epoch_func=lambda c, _: {"throughput": float(c["bs"] * c["nw"])},
        )
        return searcher.search(search_space={"bs": [32, 64, 128], "nw": [1, 2, 4]})

    def test_finds_best_maximize(self) -> None:
        """Should find config with highest throughput."""
        result = self._make_result()
        analyzer = BestParamAnalyzer("throughput", maximize=True)
        output = analyzer.analyze(result)

        assert output["best_config"]["bs"] == 128
        assert output["best_config"]["nw"] == 4
        assert output["best_value"] == 512.0

    def test_finds_best_minimize(self) -> None:
        """Should find config with lowest throughput."""
        result = self._make_result()
        analyzer = BestParamAnalyzer("throughput", maximize=False)
        output = analyzer.analyze(result)

        assert output["best_config"]["bs"] == 32
        assert output["best_config"]["nw"] == 1

    def test_all_values_returned(self) -> None:
        """all_values should contain all (config, value) pairs."""
        result = self._make_result()
        analyzer = BestParamAnalyzer("throughput")
        output = analyzer.analyze(result)

        assert len(output["all_values"]) == 9  # 3 x 3


class TestChartAnalyzer:
    """Test ChartAnalyzer."""

    def test_generates_chart_file(self) -> None:
        """ChartAnalyzer should save a chart to the given path."""
        searcher = ParamSearcher(
            init_func=lambda c: None,
            epoch_func=lambda c, _: {"speed": float(c["x"])},
        )
        result = searcher.search(search_space={"x": [1, 2, 3, 4]})

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name

        try:
            analyzer = ChartAnalyzer(
                metric_name="speed",
                x_param="x",
                save_path=path,
            )
            output = analyzer.analyze(result)
            assert output["chart_path"] == path
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_grouped_chart(self) -> None:
        """ChartAnalyzer with group_param should handle grouping."""
        searcher = ParamSearcher(
            init_func=lambda c: None,
            epoch_func=lambda c, _: {"speed": float(c["bs"] * c["nw"])},
        )
        result = searcher.search(search_space={"bs": [32, 64], "nw": [1, 2]})

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name

        try:
            analyzer = ChartAnalyzer(
                metric_name="speed",
                x_param="bs",
                group_param="nw",
                save_path=path,
            )
            output = analyzer.analyze(result)
            assert output["chart_path"] == path
            assert "nw" in output["data"]
        finally:
            os.unlink(path)
