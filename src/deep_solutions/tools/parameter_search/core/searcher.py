"""Core parameter searcher using itertools.product for exhaustive search."""

import itertools
import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Set

from deep_solutions._utils.metrics import (
    MetricsCollector,
    MetricsRecord,
)

logger = logging.getLogger(__name__)

# Type aliases for clarity
Config = Dict[str, Any]
Metrics = Dict[str, float]
InitFunc = Callable[[Config], Any]
EpochFunc = Callable[[Config, Any], Metrics]


class SearchResult:
    """Result of a parameter search run.

    Contains all metrics records and provides convenience accessors
    for the best configuration.

    Args:
        collector: MetricsCollector with all search results.
        search_space: The search space that was explored.
    """

    def __init__(
        self,
        collector: MetricsCollector,
        search_space: Dict[str, Sequence[Any]],
    ) -> None:
        self._collector = collector
        self.search_space = search_space

    @property
    def records(self) -> List[MetricsRecord]:
        """All metrics records from the search."""
        return self._collector.get_records()

    @property
    def collector(self) -> MetricsCollector:
        """The underlying MetricsCollector."""
        return self._collector

    def get_best(
        self,
        metric_name: str,
        maximize: bool = True,
    ) -> Optional[MetricsRecord]:
        """Get the best record for a given metric.

        Args:
            metric_name: Name of the metric to optimize.
            maximize: If True, find maximum; if False, find minimum.

        Returns:
            The best MetricsRecord, or None if no records exist.
        """
        return self._collector.get_best(metric_name, maximize)

    def to_list(self) -> List[Dict[str, Any]]:
        """Convert all records to list of dictionaries."""
        return self._collector.to_list()

    def __len__(self) -> int:
        return len(self._collector)


class ParamSearcher:
    """Generic parameter searcher that iterates over search spaces.

    Uses the Strategy pattern: users provide init_func and epoch_func
    callables that define the initialization and evaluation behavior.

    Example:
        >>> def my_init(config):
        ...     return create_model(config)
        >>> def my_epoch(config, model):
        ...     return {"loss": train_one_epoch(model)}
        >>> searcher = ParamSearcher(
        ...     init_func=my_init,
        ...     epoch_func=my_epoch,
        ...     num_epochs=3,
        ... )
        >>> result = searcher.search(
        ...     search_space={"lr": [0.01, 0.1], "batch_size": [32, 64]},
        ... )
        >>> best = result.get_best("loss", maximize=False)

    Args:
        init_func: Callable that receives a config dict and returns
            an initialized resource (e.g., model, dataloader).
        epoch_func: Callable that receives (config, init_result) and
            returns a metrics dict with float values.
        num_epochs: Number of epochs to run per configuration.
        cleanup_func: Optional callable for cleanup after each config.
            Receives (config, init_result).
    """

    def __init__(
        self,
        init_func: InitFunc,
        epoch_func: EpochFunc,
        num_epochs: int = 1,
        cleanup_func: Optional[Callable[[Config, Any], None]] = None,
    ) -> None:
        if num_epochs < 1:
            raise ValueError("num_epochs must be >= 1")

        self._init_func = init_func
        self._epoch_func = epoch_func
        self._num_epochs = num_epochs
        self._cleanup_func = cleanup_func

    def search(
        self,
        search_space: Dict[str, Sequence[Any]],
        fixed_config: Optional[Config] = None,
    ) -> SearchResult:
        """Execute exhaustive search over the parameter space.

        Iterates over all combinations of parameters in search_space
        using itertools.product. For each combination:
        1. Merges with fixed_config
        2. Calls init_func to create resources
        3. Calls epoch_func num_epochs times
        4. Aggregates metrics (mean across epochs)
        5. Optionally calls cleanup_func

        Args:
            search_space: Dict mapping parameter names to lists of values.
                Example: {"lr": [0.01, 0.1], "batch_size": [32, 64]}
            fixed_config: Optional fixed parameters merged into each config.

        Returns:
            SearchResult containing all metrics and best configurations.

        Raises:
            ValueError: If search_space is empty.
        """
        if not search_space:
            raise ValueError("search_space must not be empty")

        collector = MetricsCollector()
        param_names = list(search_space.keys())
        param_values = list(search_space.values())

        total = 1
        for vals in param_values:
            total *= len(vals)

        logger.info(
            "Starting parameter search: %d combinations, %d epochs each",
            total,
            self._num_epochs,
        )

        for i, combo in enumerate(itertools.product(*param_values)):
            config: Config = dict(zip(param_names, combo))
            if fixed_config:
                config = {**fixed_config, **config}

            logger.info(
                "Config %d/%d: %s",
                i + 1,
                total,
                config,
            )

            # Initialize resources
            init_result = self._init_func(config)

            # Run epochs and collect metrics
            epoch_metrics_list: List[Metrics] = []
            for _epoch_idx in range(self._num_epochs):
                metrics = self._epoch_func(config, init_result)
                epoch_metrics_list.append(metrics)

            # Aggregate metrics across epochs (mean)
            aggregated = self._aggregate_metrics(epoch_metrics_list)
            collector.add(config=config, metrics=aggregated)

            # Cleanup
            if self._cleanup_func is not None:
                self._cleanup_func(config, init_result)

        logger.info("Parameter search complete: %d configurations tested", total)
        return SearchResult(collector=collector, search_space=search_space)

    @staticmethod
    def _aggregate_metrics(
        metrics_list: List[Metrics],
    ) -> Metrics:
        """Aggregate metrics across multiple epochs by computing mean.

        Args:
            metrics_list: List of metrics dicts from each epoch.

        Returns:
            Aggregated metrics dictionary.
        """
        if not metrics_list:
            return {}

        all_keys: Set[str] = set()
        for m in metrics_list:
            all_keys.update(m.keys())

        result: Metrics = {}
        for key in all_keys:
            values = [m[key] for m in metrics_list if key in m]
            result[key] = sum(values) / len(values)

        return result
