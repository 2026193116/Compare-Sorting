"""Public Python sorting API.

The registry is the single list that callers use to run every algorithm.
"""

from cocktail_shaker_sort import cocktail_shaker_sort
from counting_sort import counting_sort
from shell_sort import shell_sort

SORT_ALGORITHMS = [
    ("shell_sort", shell_sort),
    ("counting_sort", counting_sort),
    ("cocktail_shaker_sort", cocktail_shaker_sort),
]

__all__ = [
    "SORT_ALGORITHMS",
    "shell_sort",
    "counting_sort",
    "cocktail_shaker_sort",
]
