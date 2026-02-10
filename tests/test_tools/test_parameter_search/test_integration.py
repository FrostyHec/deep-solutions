"""Tests for top-level imports and version check."""

import deep_solutions
from deep_solutions.tools.parameter_search import ParamSearcher, SearchResult, Timer


def test_version_check() -> None:
    """Library version should be accessible and non-empty."""
    version = deep_solutions.get_library_version()
    assert isinstance(version, str)
    assert len(version) > 0
    assert version == deep_solutions.__version__


def test_top_level_imports() -> None:
    """Core API should be importable from top-level parameter_search."""
    assert ParamSearcher is not None
    assert SearchResult is not None
    assert Timer is not None


def test_submodule_imports() -> None:
    """Sub-module APIs should be importable."""
    from deep_solutions.tools.parameter_search.analyzers import (
        BaseAnalyzer,
        BestParamAnalyzer,
        ChartAnalyzer,
    )
    from deep_solutions.tools.parameter_search.epochs import simple_epoch, timed_epoch

    assert BaseAnalyzer is not None
    assert BestParamAnalyzer is not None
    assert ChartAnalyzer is not None
    assert timed_epoch is not None
    assert simple_epoch is not None
