"""Decorators for marking public API entries."""

from typing import TypeVar

T = TypeVar("T")


def public_api(func_or_class: T) -> T:
    """Mark a function or class as part of the public API.

    This decorator is used to explicitly mark exported functions and classes
    that should be part of the library's public interface.

    Args:
        func_or_class: Function or class to mark as public API.

    Returns:
        The marked function or class unchanged.
    """
    if hasattr(func_or_class, "__doc__"):
        func_or_class.__doc__ = f"[PUBLIC API] {func_or_class.__doc__ or ''}"
    return func_or_class
