"""Shell sort implementation with gap = n/4, gap /= 2 sequence."""


def shell_sort(values):
    """Return a sorted copy using shell sort.
    
    Uses a gap sequence starting from n/4 and halving each iteration.
    Implements insertion sort with variable gap to efficiently move
    elements toward their final positions.
    """
    result = list(values)
    n = len(result)
    gap = max(1, n // 4)
    
    while gap > 0:
        # Perform gap insertion sort
        for index in range(gap, n):
            value = result[index]
            j = index
            while j >= gap and result[j - gap] > value:
                result[j] = result[j - gap]
                j -= gap
            result[j] = value
        gap //= 2
    
    return result
