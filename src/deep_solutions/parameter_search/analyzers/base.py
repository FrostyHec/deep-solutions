"""Base analyzer interface for parameter search results."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from deep_solutions.parameter_search.core.searcher import SearchResult


class BaseAnalyzer(ABC):
    """Abstract base class for search result analyzers.

    Subclass this to create custom analyzers. Each analyzer receives
    a SearchResult and produces analysis output.
    """

    @abstractmethod
    def analyze(self, result: SearchResult) -> Dict[str, Any]:
        """Analyze search results.

        Args:
            result: SearchResult containing all metrics records.

        Returns:
            Dictionary with analysis output (format depends on analyzer).
        """
        ...
