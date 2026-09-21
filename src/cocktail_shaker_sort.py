"""Cocktail shaker sort implementation."""


def cocktail_shaker_sort(values):
    """Return a sorted copy using bidirectional bubble-sort passes."""
    result = list(values)
    left = 0
    right = len(result) - 1

    while left < right:
        swapped = False

        for index in range(left, right):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True

        right -= 1
        for index in range(right, left, -1):
            if result[index - 1] > result[index]:
                result[index - 1], result[index] = result[index], result[index - 1]
                swapped = True

        left += 1
        if not swapped:
            break

    return result
