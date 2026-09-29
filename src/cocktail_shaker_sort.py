"""Cocktail shaker sort implementation using bidirectional bubble passes."""


def cocktail_shaker_sort(values, stats=None):
    """Return a sorted copy, optionally updating stats."""
    result = list(values)
    left = 0
    right = len(result) - 1

    if stats is not None:
        stats["comparisons"] = 0
        stats["moves"] = 0

    while left < right:
        swapped = False

        for index in range(left, right):
            if stats is not None:
                stats["comparisons"] += 1
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                if stats is not None:
                    stats["moves"] += 3
                swapped = True

        if not swapped:
            break

        right -= 1

        for index in range(right, left, -1):
            if stats is not None:
                stats["comparisons"] += 1
            if result[index - 1] > result[index]:
                result[index - 1], result[index] = result[index], result[index - 1]
                if stats is not None:
                    stats["moves"] += 3
                swapped = True

        left += 1

    return result
