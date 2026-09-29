"""Shared statistics for Python sorting implementations."""

from dataclasses import dataclass


@dataclass
class SortStats:
    """Counters shared by all Python sorting implementations."""

    comparisons: int = 0
    moves: int = 0
