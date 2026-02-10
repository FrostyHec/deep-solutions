"""Tests for parameter search core: ParamSearcher and SearchResult."""

from deep_solutions.tools.parameter_search.core.searcher import ParamSearcher


class TestParamSearcher:
    """Test ParamSearcher exhaustive search over parameter space."""

    def test_search_iterates_all_combinations(self) -> None:
        """Verify all param combos are visited via itertools.product."""
        visited = []

        def init_fn(config):
            return config

        def epoch_fn(config, init_result):
            visited.append(dict(config))
            return {"score": config["a"] + config["b"]}

        searcher = ParamSearcher(init_func=init_fn, epoch_func=epoch_fn, num_epochs=1)
        result = searcher.search(search_space={"a": [1, 2], "b": [10, 20]})

        assert len(visited) == 4  # 2 x 2
        configs = [r.config for r in result.records]
        assert {"a": 1, "b": 10} in configs
        assert {"a": 2, "b": 20} in configs

    def test_multi_epoch_aggregation(self) -> None:
        """Verify metrics are averaged across epochs."""
        call_count = 0

        def init_fn(config):
            return None

        def epoch_fn(config, _):
            nonlocal call_count
            call_count += 1
            # Return different values each epoch
            return {"val": float(call_count)}

        searcher = ParamSearcher(init_func=init_fn, epoch_func=epoch_fn, num_epochs=3)
        result = searcher.search(search_space={"x": [1]})

        assert call_count == 3
        record = result.records[0]
        # Epochs returned 1.0, 2.0, 3.0 -> mean = 2.0
        assert record.metrics["val"] == 2.0

    def test_fixed_config_merged(self) -> None:
        """Verify fixed_config is merged into each configuration."""
        captured = []

        def init_fn(config):
            captured.append(dict(config))
            return None

        def epoch_fn(config, _):
            return {"m": 1.0}

        searcher = ParamSearcher(init_func=init_fn, epoch_func=epoch_fn)
        searcher.search(
            search_space={"a": [1, 2]},
            fixed_config={"fixed_key": "fixed_val"},
        )

        assert all(c["fixed_key"] == "fixed_val" for c in captured)

    def test_cleanup_func_called(self) -> None:
        """Verify cleanup_func is called after each config."""
        cleaned = []

        def init_fn(config):
            return {"resource": config["x"]}

        def epoch_fn(config, res):
            return {"m": 1.0}

        def cleanup(config, res):
            cleaned.append(res["resource"])

        searcher = ParamSearcher(
            init_func=init_fn, epoch_func=epoch_fn, cleanup_func=cleanup
        )
        searcher.search(search_space={"x": [10, 20]})

        assert cleaned == [10, 20]

    def test_empty_search_space_raises(self) -> None:
        """Empty search_space should raise ValueError."""
        import pytest

        searcher = ParamSearcher(init_func=lambda c: None, epoch_func=lambda c, r: {})
        with pytest.raises(ValueError):
            searcher.search(search_space={})

    def test_invalid_num_epochs_raises(self) -> None:
        """num_epochs < 1 should raise ValueError."""
        import pytest

        with pytest.raises(ValueError):
            ParamSearcher(
                init_func=lambda c: None,
                epoch_func=lambda c, r: {},
                num_epochs=0,
            )


class TestSearchResult:
    """Test SearchResult accessors."""

    def test_get_best_maximize(self) -> None:
        """Find config with highest metric value."""
        searcher = ParamSearcher(
            init_func=lambda c: None,
            epoch_func=lambda c, _: {"score": float(c["x"])},
        )
        result = searcher.search(search_space={"x": [1, 5, 3]})

        best = result.get_best("score", maximize=True)
        assert best is not None
        assert best.config["x"] == 5

    def test_get_best_minimize(self) -> None:
        """Find config with lowest metric value."""
        searcher = ParamSearcher(
            init_func=lambda c: None,
            epoch_func=lambda c, _: {"loss": float(c["x"])},
        )
        result = searcher.search(search_space={"x": [10, 2, 7]})

        best = result.get_best("loss", maximize=False)
        assert best is not None
        assert best.config["x"] == 2

    def test_to_list(self) -> None:
        """Verify serialization to list of dicts."""
        searcher = ParamSearcher(
            init_func=lambda c: None,
            epoch_func=lambda c, _: {"m": 1.0},
        )
        result = searcher.search(search_space={"x": [1]})

        data = result.to_list()
        assert len(data) == 1
        assert "config" in data[0]
        assert "metrics" in data[0]
        assert "timestamp" in data[0]
