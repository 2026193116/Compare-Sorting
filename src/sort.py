def shell_sort(values):
    a = list(values); gap = 1
    while gap < len(a) // 3: gap = gap * 3 + 1
    while gap:
        for i in range(gap, len(a)):
            value, j = a[i], i
            while j >= gap and a[j-gap] > value:
                a[j] = a[j-gap]; j -= gap
            a[j] = value
        gap = (gap - 1) // 3
    return a

def counting_sort(values):
    if not values: return []
    lo, hi = min(values), max(values); count = [0] * (hi-lo+1)
    for value in values: count[value-lo] += 1
    result = []
    for offset, amount in enumerate(count): result.extend([offset+lo] * amount)
    return result

def cocktail_shaker_sort(values):
    a = list(values); left, right = 0, len(a)-1
    while left < right:
        swapped = False
        for i in range(left, right):
            if a[i] > a[i+1]: a[i], a[i+1] = a[i+1], a[i]; swapped = True
        right -= 1
        for i in range(right, left, -1):
            if a[i-1] > a[i]: a[i-1], a[i] = a[i], a[i-1]; swapped = True
        left += 1
        if not swapped: break
    return a

SORT_ALGORITHMS = [("shell_sort", shell_sort), ("counting_sort", counting_sort), ("cocktail_shaker_sort", cocktail_shaker_sort)]
