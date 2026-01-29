"""
Utility functions for deep-solutions package.
"""


def format_output(data, prefix: str = "Result"):
    """
    Format output data with a prefix.

    Args:
        data: Data to format.
        prefix: Prefix string.

    Returns:
        str: Formatted output.
    """
    return f"{prefix}: {data}"


def _internal_helper():
    """
    Internal helper function (not exposed in public API).
    """
    return "Internal use only"
