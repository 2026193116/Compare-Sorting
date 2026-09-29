const SortAlgorithm SORT_ALGORITHMS[] = {
    {
        "shellSort",
        "gap-dependent; O(n^2) worst for this sequence",
        "O(1)",
        0,
        shellSort
    },
    {
        "countingSort",
        "O(n + k)",
        "O(n + k)",
        1,
        countingSort
    },
    {
        "cocktailShakerSort",
        "O(n^2)",
        "O(1)",
        1,
        cocktailShakerSort
    }
};
