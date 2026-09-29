"""Shell sort implementation."""

from sort_stats import SortStats


def shell_sort(values, stats=None, *, copy_input=True):
    """Return a sorted copy using the same gap sequence as the C version."""
    if stats is None:
        stats = SortStats()

    result = list(values) if copy_input else values
    n = len(result)

    gap = n // 4
    if gap == 0:
        gap = 1

    while gap > 0:
        for index in range(gap, n):
            value = result[index]
            position = index

            while position >= gap:
                stats.comparisons += 1

                if result[position - gap] <= value:
                    break

                result[position] = result[position - gap]
                stats.moves += 1
                position -= gap

            if position != index:
                result[position] = value
                stats.moves += 1

        gap //= 2

    return result
