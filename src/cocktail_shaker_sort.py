"""Cocktail shaker sort implementation (bidirectional bubble sort)."""

from sort_stats import SortStats


def cocktail_shaker_sort(values, stats=None, *, copy_input=True):
    """Return a sorted copy using cocktail shaker sort."""
    if stats is None:
        stats = SortStats()

    result = list(values) if copy_input else values
    left = 0
    right = len(result) - 1

    while left < right:
        swapped = False

        # Left-to-right pass: move the largest value to the right.
        for index in range(left, right):
            stats.comparisons += 1

            if result[index] > result[index + 1]:
                result[index], result[index + 1] = (
                    result[index + 1],
                    result[index],
                )
                stats.moves += 3
                swapped = True

        if not swapped:
            break

        right -= 1
        swapped = False

        # Right-to-left pass: move the smallest value to the left.
        for index in range(right, left, -1):
            stats.comparisons += 1

            if result[index - 1] > result[index]:
                result[index - 1], result[index] = (
                    result[index],
                    result[index - 1],
                )
                stats.moves += 3
                swapped = True

        left += 1

        # Stop if the backward pass made no swaps.
        if not swapped:
            break

    return result
