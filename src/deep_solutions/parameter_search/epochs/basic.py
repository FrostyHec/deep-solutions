"""Built-in epoch implementations for common use cases."""

from typing import Any, Callable, Dict

from deep_solutions.parameter_search.utils.timer import Timer

# Metrics dictionary type
Metrics = Dict[str, float]


def timed_epoch(
    run_func: Callable[[Dict[str, Any], Any], int],
    repeats: int = 3,
) -> Callable[[Dict[str, Any], Any], Metrics]:
    """Create a timed epoch function that measures throughput.

    Wraps a user-provided function with timing logic. The user function
    should process data and return the number of samples processed.

    Args:
        run_func: Callable(config, init_result) -> n_samples processed.
        repeats: Number of repetitions to average over.

    Returns:
        Epoch function that returns throughput metrics.

    Example:
        >>> def process(config, loader):
        ...     count = 0
        ...     for batch in loader:
        ...         count += len(batch)
        ...     return count
        >>> epoch_fn = timed_epoch(process, repeats=3)
    """
    if repeats < 1:
        raise ValueError("repeats must be >= 1")

    def _epoch(config: Dict[str, Any], init_result: Any) -> Metrics:
        timer = Timer(start_immediately=False)
        speeds = []

        for _ in range(repeats):
            timer.start()
            n_samples = run_func(config, init_result)
            elapsed = timer.stop()
            if elapsed > 0:
                speeds.append(n_samples / elapsed)
            else:
                speeds.append(float("inf"))

        mean_speed = sum(speeds) / len(speeds)
        stats = timer.get_stats()

        return {
            "throughput": mean_speed,
            "mean_time": stats["average"],
            "total_time": stats["total"],
        }

    return _epoch


def simple_epoch(
    eval_func: Callable[[Dict[str, Any], Any], Metrics],
) -> Callable[[Dict[str, Any], Any], Metrics]:
    """Create a simple epoch that delegates directly to eval_func.

    Use this when you want full control over metrics computation.

    Args:
        eval_func: Callable(config, init_result) -> metrics dict.

    Returns:
        The eval_func itself (identity wrapper for consistency).
    """
    return eval_func
