"""Counting sort implementation."""


def counting_sort(values):
    """Return a sorted copy of integer values, including negative values."""
    result = list(values)
    if not result:
        return []

    minimum = min(result)
    maximum = max(result)
    counts = [0] * (maximum - minimum + 1)

    for value in result:
        counts[value - minimum] += 1

    sorted_values = []
    for offset, amount in enumerate(counts):
        sorted_values.extend([offset + minimum] * amount)
    return sorted_values
