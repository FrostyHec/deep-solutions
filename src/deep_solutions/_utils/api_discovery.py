"""
Dynamic API discovery utilities for deep-solutions.

Automatically discovers and collects all functions and classes decorated with
@public_api across the package.
"""

import importlib
import inspect
import pkgutil
from typing import Any, Dict, List, Set


def _is_public_api(obj: Any) -> bool:
    """
    Check if an object is marked with @public_api decorator.

    Args:
        obj: Any Python object (function, class, etc.)

    Returns:
        True if the object's docstring contains [PUBLIC API] marker.
    """
    docstring = inspect.getdoc(obj)
    return docstring is not None and "[PUBLIC API]" in docstring


def discover_public_apis(package_name: str = "deep_solutions.tools") -> Dict[str, Any]:
    """
    Discover all public APIs in the tools package.

    Recursively walks through all modules in the tools package and collects
    objects (functions, classes) that are decorated with @public_api.

    Args:
        package_name: Package to scan for public APIs. Defaults to "deep_solutions.tools".

    Returns:
        Dictionary mapping API names to their objects.
    """
    public_apis: Dict[str, Any] = {}
    visited_modules: Set[str] = set()

    try:
        package = importlib.import_module(package_name)
    except ImportError:
        return public_apis

    # Get package path
    if not hasattr(package, "__path__"):
        return public_apis

    package_path = package.__path__

    # Walk through all modules in the package
    for _importer, modname, _ispkg in pkgutil.walk_packages(
        path=package_path, prefix=f"{package_name}."
    ):
        if modname in visited_modules:
            continue

        visited_modules.add(modname)

        try:
            module = importlib.import_module(modname)
        except (ImportError, AttributeError):
            continue

        # Inspect module members
        for name, obj in inspect.getmembers(module):
            # Skip private members
            if name.startswith("_"):
                continue

            # Check if it's a public API
            if _is_public_api(obj):
                # Avoid duplicates - use the shortest name
                if name not in public_apis:
                    public_apis[name] = obj

    return public_apis


def get_public_api_names(package_name: str = "deep_solutions.tools") -> List[str]:
    """
    Get list of all public API names.

    Args:
        package_name: Package to scan. Defaults to "deep_solutions.tools".

    Returns:
        Sorted list of public API names.
    """
    apis = discover_public_apis(package_name)
    return sorted(apis.keys())
