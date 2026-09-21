"""Shell sort implementation."""


def shell_sort(values):
    """Return a sorted copy using Knuth's gap sequence."""
    result = list(values)
    gap = 1
    while gap < len(result) // 3:
        gap = gap * 3 + 1

    while gap > 0:
        for index in range(gap, len(result)):
            value = result[index]
            position = index
            while position >= gap and result[position - gap] > value:
                result[position] = result[position - gap]
                position -= gap
            result[position] = value
        gap = (gap - 1) // 3

    return result
