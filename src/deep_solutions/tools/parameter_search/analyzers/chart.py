"""Chart analyzer for visualizing parameter search results."""

import logging
from typing import Any, Dict, Optional

from deep_solutions.tools.parameter_search.analyzers.base import BaseAnalyzer
from deep_solutions.tools.parameter_search.core.searcher import SearchResult

logger = logging.getLogger(__name__)


class ChartAnalyzer(BaseAnalyzer):
    """Generate parameter sweep charts using matplotlib.

    Plots metric values across parameter combinations. Supports
    grouping by one parameter and plotting against another.

    Args:
        metric_name: Name of the metric to plot on Y-axis.
        x_param: Parameter name for X-axis.
        group_param: Optional parameter name to group curves by.
        title: Chart title. Auto-generated if None.
        save_path: File path to save the chart. If None, uses show().
        use_log_x: If True, use log2 scale for X-axis.
        figsize: Figure size as (width, height).

    Example:
        >>> analyzer = ChartAnalyzer(
        ...     metric_name="throughput",
        ...     x_param="batch_size",
        ...     group_param="num_workers",
        ...     save_path="speed_chart.png",
        ... )
        >>> output = analyzer.analyze(result)
    """

    def __init__(
        self,
        metric_name: str,
        x_param: str,
        group_param: Optional[str] = None,
        title: Optional[str] = None,
        save_path: Optional[str] = None,
        use_log_x: bool = False,
        figsize: tuple = (10, 6),
    ) -> None:
        self._metric_name = metric_name
        self._x_param = x_param
        self._group_param = group_param
        self._title = title
        self._save_path = save_path
        self._use_log_x = use_log_x
        self._figsize = figsize

    def analyze(self, result: SearchResult) -> Dict[str, Any]:
        """Generate chart from search results.

        Args:
            result: SearchResult containing all metrics records.

        Returns:
            Dictionary with keys:
                - chart_path: Path where chart was saved (or None)
                - data: Organized data used for plotting
        """
        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            logger.warning(
                "matplotlib not installed. Skipping chart generation. "
                "Install with: pip install matplotlib"
            )
            return {"chart_path": None, "data": {}, "error": "matplotlib not installed"}

        data = self._organize_data(result)

        fig, ax = plt.subplots(figsize=self._figsize)

        if self._group_param and self._group_param in data:
            for group_val, points in sorted(data[self._group_param].items()):
                x_vals = [p[0] for p in points]
                y_vals = [p[1] for p in points]
                label = f"{self._group_param}={group_val}"
                ax.plot(x_vals, y_vals, marker="o", label=label)
            ax.legend()
        else:
            # No grouping - single line
            points = data.get("_ungrouped", [])
            x_vals = [p[0] for p in points]
            y_vals = [p[1] for p in points]
            ax.plot(x_vals, y_vals, marker="o")

        title = self._title or (f"{self._metric_name} vs {self._x_param}")
        ax.set_title(title)
        ax.set_xlabel(self._x_param)
        ax.set_ylabel(self._metric_name)
        ax.grid(True, linestyle="--", alpha=0.4)

        if self._use_log_x:
            ax.set_xscale("log", base=2)

        plt.tight_layout()

        chart_path = None
        if self._save_path:
            chart_path = self._save_path
            plt.savefig(chart_path, dpi=150)
            logger.info("Chart saved to %s", chart_path)

        plt.close(fig)

        return {"chart_path": chart_path, "data": data}

    def _organize_data(self, result: SearchResult) -> Dict[str, Any]:
        """Organize records into plottable data structure.

        Args:
            result: SearchResult to organize.

        Returns:
            Organized data dictionary.
        """
        data: Dict[str, Any] = {}

        for record in result.records:
            if self._metric_name not in record.metrics:
                continue

            x_val = record.config.get(self._x_param)
            y_val = record.metrics[self._metric_name]

            if x_val is None:
                continue

            if self._group_param:
                group_val = record.config.get(self._group_param)
                if self._group_param not in data:
                    data[self._group_param] = {}
                if group_val not in data[self._group_param]:
                    data[self._group_param][group_val] = []
                data[self._group_param][group_val].append((x_val, y_val))
            else:
                if "_ungrouped" not in data:
                    data["_ungrouped"] = []
                data["_ungrouped"].append((x_val, y_val))

        return data
