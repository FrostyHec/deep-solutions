"""Tests for parameter search utilities: Timer, MetricsCollector, decorators."""

import time

from deep_solutions.parameter_search.utils.decorators import public_api
from deep_solutions.parameter_search.utils.metrics import (
    MetricsCollector,
    MetricsRecord,
)
from deep_solutions.parameter_search.utils.timer import Timer


class TestTimer:
    """Test Timer utility."""

    def test_start_stop_returns_elapsed(self) -> None:
        """Timer should measure elapsed time."""
        timer = Timer(start_immediately=False)
        timer.start()
        time.sleep(0.05)
        elapsed = timer.stop()
        assert elapsed > 0.01

    def test_multiple_laps(self) -> None:
        """Timer should track multiple laps."""
        timer = Timer(start_immediately=False)
        for _ in range(3):
            timer.start()
            time.sleep(0.01)
            timer.stop()

        laps = timer.get_laps()
        assert len(laps) == 3
        assert all(lap > 0 for lap in laps)

    def test_get_stats(self) -> None:
        """Stats should include total, count, average, min, max."""
        timer = Timer(start_immediately=False)
        timer.start()
        time.sleep(0.01)
        timer.stop()

        stats = timer.get_stats()
        assert stats["count"] == 1
        assert stats["total"] > 0
        assert stats["average"] > 0
        assert stats["min"] > 0
        assert stats["max"] > 0

    def test_stop_without_start_raises(self) -> None:
        """Stopping without starting should raise RuntimeError."""
        import pytest

        timer = Timer(start_immediately=False)
        with pytest.raises(RuntimeError):
            timer.stop()

    def test_reset(self) -> None:
        """Reset should clear all data."""
        timer = Timer()
        time.sleep(0.01)
        timer.stop()
        timer.reset()
        assert timer.get_laps() == []
        assert timer.get_accumulated() == 0.0

    def test_empty_stats(self) -> None:
        """Stats with no laps should return zeros."""
        timer = Timer(start_immediately=False)
        stats = timer.get_stats()
        assert stats["count"] == 0
        assert stats["total"] == 0.0


class TestMetricsCollector:
    """Test MetricsCollector."""

    def test_add_and_get_records(self) -> None:
        """Add records and retrieve them."""
        collector = MetricsCollector()
        collector.add(config={"a": 1}, metrics={"score": 10.0})
        collector.add(config={"a": 2}, metrics={"score": 20.0})

        assert len(collector) == 2
        records = collector.get_records()
        assert records[0].config["a"] == 1
        assert records[1].metrics["score"] == 20.0

    def test_get_best_maximize(self) -> None:
        """Find record with highest metric."""
        collector = MetricsCollector()
        collector.add(config={"x": 1}, metrics={"val": 5.0})
        collector.add(config={"x": 2}, metrics={"val": 15.0})
        collector.add(config={"x": 3}, metrics={"val": 10.0})

        best = collector.get_best("val", maximize=True)
        assert best is not None
        assert best.config["x"] == 2

    def test_get_best_minimize(self) -> None:
        """Find record with lowest metric."""
        collector = MetricsCollector()
        collector.add(config={"x": 1}, metrics={"val": 5.0})
        collector.add(config={"x": 2}, metrics={"val": 15.0})

        best = collector.get_best("val", maximize=False)
        assert best is not None
        assert best.config["x"] == 1

    def test_get_best_empty(self) -> None:
        """Empty collector returns None."""
        collector = MetricsCollector()
        assert collector.get_best("val") is None

    def test_get_best_missing_metric(self) -> None:
        """If no record has the metric, return None."""
        collector = MetricsCollector()
        collector.add(config={"x": 1}, metrics={"other": 5.0})
        assert collector.get_best("nonexistent") is None

    def test_to_list(self) -> None:
        """to_list returns list of dicts."""
        collector = MetricsCollector()
        collector.add(config={"a": 1}, metrics={"m": 1.0})
        data = collector.to_list()
        assert len(data) == 1
        assert data[0]["config"] == {"a": 1}

    def test_clear(self) -> None:
        """Clear removes all records."""
        collector = MetricsCollector()
        collector.add(config={}, metrics={"m": 1.0})
        collector.clear()
        assert len(collector) == 0


class TestMetricsRecord:
    """Test MetricsRecord serialization."""

    def test_to_dict(self) -> None:
        """Record should serialize with config, metrics, timestamp."""
        record = MetricsRecord(config={"lr": 0.01}, metrics={"loss": 0.5})
        d = record.to_dict()
        assert d["config"] == {"lr": 0.01}
        assert d["metrics"] == {"loss": 0.5}
        assert "timestamp" in d


class TestPublicApiDecorator:
    """Test @public_api decorator."""

    def test_marks_function(self) -> None:
        """Decorator should mark function docstring."""

        @public_api
        def my_func():
            """My function."""
            pass

        assert "[PUBLIC API]" in (my_func.__doc__ or "")

    def test_marks_class(self) -> None:
        """Decorator should mark class docstring."""

        @public_api
        class MyClass:
            """My class."""

            pass

        assert "[PUBLIC API]" in (MyClass.__doc__ or "")

    def test_preserves_behavior(self) -> None:
        """Decorated function should work normally."""

        @public_api
        def add(a, b):
            """Add two numbers."""
            return a + b

        assert add(1, 2) == 3
