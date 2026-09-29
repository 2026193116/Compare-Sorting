"""Public Python sorting API."""

from cocktail_shaker_sort import cocktail_shaker_sort
from counting_sort import counting_sort
from shell_sort import shell_sort


SORT_ALGORITHMS = [
    ("shellSort", shell_sort),
    ("countingSort", counting_sort),
    ("cocktailShakerSort", cocktail_shaker_sort),
]

__all__ = [
    "SORT_ALGORITHMS",
    "shell_sort",
    "counting_sort",
    "cocktail_shaker_sort",
]
