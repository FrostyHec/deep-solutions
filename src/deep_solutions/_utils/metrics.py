"""Metrics collection utilities."""

from datetime import datetime
from typing import Any, Dict, List, Optional


class MetricsRecord:
    """A single record of metrics for a parameter configuration.

    Args:
        config: Parameter configuration dictionary.
        metrics: Collected metrics dictionary.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        metrics: Dict[str, float],
    ) -> None:
        self.config = config
        self.metrics = metrics
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary.

        Returns:
            Dictionary with config, metrics, and timestamp.
        """
        return {
            "config": self.config,
            "metrics": self.metrics,
            "timestamp": self.timestamp,
        }


class MetricsCollector:
    """Collect and manage metrics records from parameter search runs.

    Provides methods to add, query, and summarize metrics.
    """

    def __init__(self) -> None:
        self._records: List[MetricsRecord] = []

    def add(
        self,
        config: Dict[str, Any],
        metrics: Dict[str, float],
    ) -> MetricsRecord:
        """Add a metrics record.

        Args:
            config: Parameter configuration.
            metrics: Collected metrics.

        Returns:
            The created MetricsRecord.
        """
        record = MetricsRecord(config=config, metrics=metrics)
        self._records.append(record)
        return record

    def get_records(self) -> List[MetricsRecord]:
        """Get all records.

        Returns:
            List of all metrics records.
        """
        return self._records.copy()

    def to_list(self) -> List[Dict[str, Any]]:
        """Convert all records to list of dictionaries.

        Returns:
            List of record dictionaries.
        """
        return [r.to_dict() for r in self._records]

    def get_best(
        self,
        metric_name: str,
        maximize: bool = True,
    ) -> Optional[MetricsRecord]:
        """Get the record with the best value for a given metric.

        Args:
            metric_name: Name of the metric to optimize.
            maximize: If True, find maximum; if False, find minimum.

        Returns:
            The best MetricsRecord, or None if no records exist.
        """
        if not self._records:
            return None

        valid = [r for r in self._records if metric_name in r.metrics]
        if not valid:
            return None

        if maximize:
            return max(valid, key=lambda r: r.metrics[metric_name])
        return min(valid, key=lambda r: r.metrics[metric_name])

    def clear(self) -> None:
        """Clear all records."""
        self._records.clear()

    def __len__(self) -> int:
        return len(self._records)
