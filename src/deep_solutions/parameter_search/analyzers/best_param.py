"""Analyzer for selecting the best parameter combination."""

from typing import Any, Dict

from deep_solutions.parameter_search.analyzers.base import BaseAnalyzer
from deep_solutions.parameter_search.core.searcher import SearchResult


class BestParamAnalyzer(BaseAnalyzer):
    """Select the best parameter combination based on a target metric.

    Args:
        metric_name: Name of the metric to optimize.
        maximize: If True, find the maximum; if False, find the minimum.

    Example:
        >>> analyzer = BestParamAnalyzer("throughput", maximize=True)
        >>> output = analyzer.analyze(result)
        >>> print(output["best_config"])  # e.g., {"batch_size": 128}
        >>> print(output["best_value"])   # e.g., 5000.0
    """

    def __init__(
        self,
        metric_name: str,
        maximize: bool = True,
    ) -> None:
        self._metric_name = metric_name
        self._maximize = maximize

    def analyze(self, result: SearchResult) -> Dict[str, Any]:
        """Find the best configuration from search results.

        Args:
            result: SearchResult containing all metrics records.

        Returns:
            Dictionary with keys:
                - best_config: Dict of parameter values
                - best_value: The optimal metric value
                - best_metrics: All metrics for the best config
                - metric_name: The metric that was optimized
                - maximize: Whether maximization was used
                - all_values: List of (config, metric_value) tuples
        """
        best = result.get_best(self._metric_name, self._maximize)

        all_values = []
        for record in result.records:
            if self._metric_name in record.metrics:
                all_values.append((record.config, record.metrics[self._metric_name]))

        output: Dict[str, Any] = {
            "metric_name": self._metric_name,
            "maximize": self._maximize,
            "all_values": all_values,
        }

        if best is not None:
            output["best_config"] = best.config
            output["best_value"] = best.metrics[self._metric_name]
            output["best_metrics"] = best.metrics
        else:
            output["best_config"] = None
            output["best_value"] = None
            output["best_metrics"] = None

        return output
