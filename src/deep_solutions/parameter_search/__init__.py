"""Parameter search library for optimizing hyperparameters.

This module provides a layered API for parameter space exploration:

**Core API** (top-level imports):
    - ``ParamSearcher``: Generic parameter searcher
    - ``SearchResult``: Search result container
    - ``Timer``: Timing utility

**Epochs** (``parameter_search.epochs``):
    - ``timed_epoch``: Throughput measurement epoch
    - ``simple_epoch``: Simple pass-through epoch

**Analyzers** (``parameter_search.analyzers``):
    - ``BaseAnalyzer``: Abstract analyzer base class
    - ``BestParamAnalyzer``: Best parameter selection
    - ``ChartAnalyzer``: Visualization charts

**PyTorch** (``parameter_search.pytorch``):
    - ``DataLoaderParamSelector``: DataLoader optimization

Example:
    Basic usage with DataLoaderParamSelector::

        from deep_solutions.parameter_search import DataLoaderParamSelector
        selector = DataLoaderParamSelector(dataset)
        result = selector.run()
        print(result["best_config"])

    Advanced usage with ParamSearcher::

        from deep_solutions.parameter_search import ParamSearcher
        searcher = ParamSearcher(init_func=my_init, epoch_func=my_epoch)
        result = searcher.search(search_space={"lr": [0.01, 0.1]})
"""

from deep_solutions.parameter_search.core.searcher import (
    ParamSearcher,
    SearchResult,
)
from deep_solutions.parameter_search.utils.timer import Timer

__all__ = [
    # Core
    "ParamSearcher",
    "SearchResult",
    # Utils
    "Timer",
]
