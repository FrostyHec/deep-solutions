"""
Internal utilities for deep-solutions.

This module contains low-level, project-agnostic utility code used internally
across the deep-solutions package. These are NOT part of the public API.

Utilities include:
- Timer: Performance timing and statistics
- MetricsCollector/MetricsRecord: Metrics tracking and management
- Decorators: Internal decorators like @public_api
- API Discovery: Dynamic public API discovery

Note: Users should NOT directly import from _utils. Use the public APIs
exposed through the tools/ packages instead.
"""

from deep_solutions._utils.api_discovery import (
    discover_public_apis,
    get_public_api_names,
)
from deep_solutions._utils.decorators import public_api
from deep_solutions._utils.metrics import MetricsCollector, MetricsRecord
from deep_solutions._utils.timer import Timer

__all__ = [
    "Timer",
    "MetricsCollector",
    "MetricsRecord",
    "public_api",
    "discover_public_apis",
    "get_public_api_names",
]
