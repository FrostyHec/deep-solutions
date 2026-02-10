"""PyTorch DataLoader parameter selection wrapper.

This module provides a high-level convenience API for finding optimal
DataLoader parameters (batch_size, num_workers, etc.). It couples
with PyTorch at this layer while the underlying search engine remains
framework-agnostic.
"""

import logging
from typing import Any, Dict, List, Optional, Sequence

from deep_solutions._utils.decorators import public_api
from deep_solutions.tools.parameter_search.analyzers.best_param import (
    BestParamAnalyzer,
)
from deep_solutions.tools.parameter_search.analyzers.chart import ChartAnalyzer
from deep_solutions.tools.parameter_search.core.searcher import (
    ParamSearcher,
)
from deep_solutions.tools.parameter_search.epochs.basic import timed_epoch

logger = logging.getLogger(__name__)

# Default search space for DataLoader parameters
DEFAULT_SEARCH_SPACE: Dict[str, List[Any]] = {
    "batch_size": [32, 64, 128, 256],
    "num_workers": [0, 2, 4, 8],
}


@public_api
class DataLoaderParamSelector:
    """Find optimal DataLoader parameters for a given dataset.

    Traverses combinations of DataLoader parameters, measures throughput,
    and identifies the best configuration. Optionally generates
    visualization charts.

    Example:
        >>> from torch.utils.data import TensorDataset
        >>> import torch
        >>> dataset = TensorDataset(torch.randn(1000, 10), torch.randn(1000))
        >>> selector = DataLoaderParamSelector(dataset)
        >>> best = selector.run()
        >>> print(best["best_config"])

    Args:
        dataset: A PyTorch Dataset instance.
        search_space: Dict mapping parameter names to lists of values.
            Defaults to batch_size=[32,64,128,256], num_workers=[0,2,4,8].
        repeats: Number of repetitions per configuration for averaging.
        batches_per_run: Max batches to process per repetition.
        fixed_params: Fixed DataLoader parameters (e.g., pin_memory=True).
        chart_path: If provided, save a throughput chart to this path.
    """

    def __init__(
        self,
        dataset: Any,
        search_space: Optional[Dict[str, Sequence[Any]]] = None,
        repeats: int = 3,
        batches_per_run: int = 50,
        fixed_params: Optional[Dict[str, Any]] = None,
        chart_path: Optional[str] = None,
    ) -> None:
        self._dataset = dataset
        self._search_space = dict(search_space or DEFAULT_SEARCH_SPACE)
        self._repeats = repeats
        self._batches_per_run = batches_per_run
        self._fixed_params = fixed_params or {}
        self._chart_path = chart_path

    def run(self) -> Dict[str, Any]:
        """Execute the parameter search and return results.

        Returns:
            Dictionary with keys:
                - best_config: Optimal parameter configuration
                - best_throughput: Throughput at the best config
                - best_metrics: All metrics for the best config
                - search_result: Full SearchResult for advanced usage
                - analysis: BestParamAnalyzer output
                - chart: ChartAnalyzer output (if chart_path was set)
        """
        try:
            from torch.utils.data import DataLoader
        except ImportError as e:
            raise ImportError(
                "PyTorch is required for DataLoaderParamSelector. "
                "Install with: pip install torch"
            ) from e

        dataset = self._dataset
        batches_per_run = self._batches_per_run
        fixed_params = self._fixed_params

        def init_func(config: Dict[str, Any]) -> Any:
            """Create DataLoader from config."""
            loader_kwargs = {**fixed_params, **config}
            batch_size = loader_kwargs.pop("batch_size", 32)
            return DataLoader(
                dataset,
                batch_size=batch_size,
                shuffle=True,
                **loader_kwargs,
            )

        def run_func(config: Dict[str, Any], loader: Any) -> int:
            """Iterate through batches and count samples."""
            n_samples = 0
            for i, batch in enumerate(loader):
                if i >= batches_per_run:
                    break
                # batch can be tensor or tuple of tensors
                if isinstance(batch, (list, tuple)):
                    n_samples += len(batch[0])
                else:
                    n_samples += len(batch)
            return n_samples

        epoch_func = timed_epoch(run_func, repeats=self._repeats)

        searcher = ParamSearcher(
            init_func=init_func,
            epoch_func=epoch_func,
            num_epochs=1,
        )

        search_result = searcher.search(
            search_space=self._search_space,
        )

        # Analyze results
        best_analyzer = BestParamAnalyzer("throughput", maximize=True)
        analysis = best_analyzer.analyze(search_result)

        output: Dict[str, Any] = {
            "best_config": analysis.get("best_config"),
            "best_throughput": analysis.get("best_value"),
            "best_metrics": analysis.get("best_metrics"),
            "search_result": search_result,
            "analysis": analysis,
        }

        # Generate chart if requested
        if self._chart_path:
            # Determine grouping: if num_workers in search space, group by it
            group_param = None
            x_param = "batch_size"
            if "num_workers" in self._search_space:
                group_param = "num_workers"
            elif len(self._search_space) > 1:
                params = list(self._search_space.keys())
                x_param = params[0]
                group_param = params[1] if len(params) > 1 else None

            chart_analyzer = ChartAnalyzer(
                metric_name="throughput",
                x_param=x_param,
                group_param=group_param,
                title="DataLoader Throughput vs Parameters",
                save_path=self._chart_path,
                use_log_x=True,
            )
            chart_output = chart_analyzer.analyze(search_result)
            output["chart"] = chart_output

        logger.info(
            "Best config: %s (throughput: %.1f samples/s)",
            output["best_config"],
            output.get("best_throughput", 0) or 0,
        )

        return output
