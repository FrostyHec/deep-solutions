"""
deep-solutions: A Python package for deep learning solutions.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

# Import from new structure
from deep_solutions.tools.helloworld import DeepSolution, format_output, hello_world


def _get_package_version() -> str:
    """Get package version, preferring installed package metadata."""
    try:
        return get_version(__name__)
    except PackageNotFoundError:
        # When not installed (only cloned source), read from setuptools-scm generated file
        try:
            from deep_solutions._version import version as scm_version

            return str(scm_version)
        except ImportError:
            return "0.0.0.dev0"


__version__: str = _get_package_version()


def get_library_version() -> str:
    """Get the library version string for quick verification.

    Returns:
        Version string of deep-solutions.

    Example:
        >>> import deep_solutions
        >>> print(deep_solutions.get_library_version())
    """
    return __version__


# Public API - explicitly list what should be exposed
__all__ = [
    "__version__",
    "hello_world",
    "DeepSolution",
    "format_output",
    "get_library_version",
]
