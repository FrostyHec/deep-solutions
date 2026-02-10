"""Built-in epoch implementations."""

from deep_solutions.parameter_search.epochs.basic import (
    simple_epoch,
    timed_epoch,
)

__all__ = [
    "timed_epoch",
    "simple_epoch",
]
