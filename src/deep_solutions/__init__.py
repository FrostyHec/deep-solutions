"""
deep-solutions: A Python package for deep learning solutions.
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

from deep_solutions._utils.api_discovery import discover_public_apis


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


# Dynamically discover and import all public APIs from tools/
_public_apis = discover_public_apis("deep_solutions.tools")

# Inject discovered APIs into module namespace
globals().update(_public_apis)

# Build __all__ dynamically
__all__ = ["__version__", "get_library_version"] + sorted(_public_apis.keys())
