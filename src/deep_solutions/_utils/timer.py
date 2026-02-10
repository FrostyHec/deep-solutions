"""Timer utility for measuring execution time."""

import time
from typing import Dict, List, Optional


class Timer:
    """Simple timer for measuring elapsed time.

    Supports multiple laps and accumulative timing. Not thread-safe.
    """

    def __init__(self, start_immediately: bool = True) -> None:
        """Initialize timer.

        Args:
            start_immediately: If True, start timing immediately.
        """
        self._start_time: Optional[float] = None
        self._laps: List[float] = []
        self._accumulated: float = 0.0

        if start_immediately:
            self.start()

    def start(self) -> None:
        """Start or resume timing."""
        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop timing and record lap time.

        Returns:
            Elapsed time in seconds since start() was called.

        Raises:
            RuntimeError: If timer was not started.
        """
        if self._start_time is None:
            raise RuntimeError("Timer was not started. Call start() first.")

        elapsed = time.perf_counter() - self._start_time
        self._laps.append(elapsed)
        self._accumulated += elapsed
        self._start_time = None
        return elapsed

    def reset(self) -> None:
        """Reset all timing data."""
        self._start_time = None
        self._laps = []
        self._accumulated = 0.0

    def get_laps(self) -> List[float]:
        """Get all recorded lap times.

        Returns:
            List of lap times in seconds.
        """
        return self._laps.copy()

    def get_accumulated(self) -> float:
        """Get total accumulated time.

        Returns:
            Total time in seconds.
        """
        return self._accumulated

    def get_average(self) -> float:
        """Get average lap time.

        Returns:
            Average lap time in seconds. Returns 0 if no laps recorded.
        """
        if not self._laps:
            return 0.0
        return self._accumulated / len(self._laps)

    def get_stats(self) -> Dict[str, float]:
        """Get comprehensive timing statistics.

        Returns:
            Dictionary with 'total', 'count', 'average', 'min', 'max'.
        """
        if not self._laps:
            return {
                "total": 0.0,
                "count": 0,
                "average": 0.0,
                "min": 0.0,
                "max": 0.0,
            }

        return {
            "total": self._accumulated,
            "count": len(self._laps),
            "average": self.get_average(),
            "min": min(self._laps),
            "max": max(self._laps),
        }
