"""Cocktail shaker sort implementation (bidirectional bubble sort)."""


def cocktail_shaker_sort(values):
    """Return a sorted copy using cocktail shaker sort.
    
    Also known as bidirectional bubble sort. Performs passes in both
    directions (left-to-right, then right-to-left) to move large values
    and small values towards their correct positions more efficiently.
    """
    result = list(values)
    left = 0
    right = len(result) - 1
    
    while left < right:
        swapped = False
        
        # Left-to-right pass: move largest to right
        for index in range(left, right):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        
        right -= 1
        
        # Right-to-left pass: move smallest to left
        for index in range(right, left, -1):
            if result[index - 1] > result[index]:
                result[index - 1], result[index] = result[index], result[index - 1]
                swapped = True
        
        left += 1
        
        # Early exit if no swaps occurred
        if not swapped:
            break
    
    return result
