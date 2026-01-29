"""
deep-solutions: A Python package for deep learning solutions.
"""

from .core import hello_world, DeepSolution
from .utils import format_output

__version__ = "0.1.0"

# Public API - explicitly list what should be exposed
__all__ = [
    "hello_world",
    "DeepSolution",
    "format_output",
]
