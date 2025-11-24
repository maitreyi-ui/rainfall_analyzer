"""
Rainfall analyzer package exposing core analysis helpers and CLI entrypoints.
"""

from .analysis import (
    DEFAULT_DRY_THRESHOLD,
    DEFAULT_HEAVY_THRESHOLD,
    RainfallSummary,
    analyze_rainfall,
)
from .cli import run_cli

__all__ = [
    "DEFAULT_DRY_THRESHOLD",
    "DEFAULT_HEAVY_THRESHOLD",
    "RainfallSummary",
    "analyze_rainfall",
    "run_cli",
]

