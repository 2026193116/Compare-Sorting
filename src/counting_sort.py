"""Counting sort implementation."""

from sort_stats import SortStats


def counting_sort(values, stats=None, *, copy_input=True):
    """Return a sorted copy using stable counting sort."""
    if stats is None:
        stats = SortStats()

    result = list(values) if copy_input else values
    n = len(result)

    if n < 2:
        return result

    minimum = result[0]
    maximum = result[0]

    # These comparisons are intentionally not included in
    # stats.comparisons to match the current C instrumentation.
    for index in range(1, n):
        if result[index] < minimum:
            minimum = result[index]
        if result[index] > maximum:
            maximum = result[index]

    range_size = maximum - minimum + 1
    counts = [0] * range_size
    output = [0] * n

    for value in result:
        counts[value - minimum] += 1

    for index in range(1, range_size):
        counts[index] += counts[index - 1]

    # Traverse from right to left to preserve stability.
    for index in range(n - 1, -1, -1):
        value = result[index]
        offset = value - minimum
        counts[offset] -= 1
        output[counts[offset]] = value

    for index in range(n):
        result[index] = output[index]
        stats.moves += 1

    return result
