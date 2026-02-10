"""
Utility functions for helloworld tool.

This module contains helper functions that support the helloworld tool's
functionality.
"""

from deep_solutions._utils.decorators import public_api


@public_api
def format_output(data, prefix: str = "Result") -> str:
    """
    Format output data with a prefix.

    Args:
        data: Data to format.
        prefix: Prefix string. Defaults to "Result".

    Returns:
        str: Formatted output string.

    Example:
        >>> format_output("success", "Status")
        'Status: success'
    """
    return f"{prefix}: {data}"


def _internal_helper():
    """
    Internal helper function (not exposed in public API).

    This demonstrates internal utility functions that support the tool
    but are not part of the public API.

    Returns:
        str: Internal marker.
    """
    return "Internal use only"
