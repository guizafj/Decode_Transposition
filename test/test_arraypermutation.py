from src.arraypermutation import ArrayPermutation

def test_create_permutation_list_of_array_with_rep_items():
    input_array = [1, 2, 2]
    permutations: list[list[int]] = ArrayPermutation.create_permutation_list_of_array_with_rep_items(input_array)
    assert len(permutations) == 27  # 3^3 combinaciones
    assert permutations[0] == [1, 1, 1]  # Primera permutación
    assert permutations[-1] == [2, 2, 2]  # Última permutación

def test_create_permutation_list_of_array_without_rep_items():
    input_array = [1, 2, 3]
    permutations = ArrayPermutation.create_permutation_list_of_array_without_rep_items(input_array)
    assert len(permutations) == 6  # 3! = 6 permutations without repetition.

def test_permute_rep_iterative():
    input_array = [1, 2]
    permutations = []
    ArrayPermutation.permute_rep_iterative(input_array, permutations)
    assert len(permutations) == 4  # 2^2 combinaciones
    assert permutations == [
        [1, 1], [1, 2],
        [2, 1], [2, 2]
    ]

def test_permute_helper():
    input_array = [1, 2, 3]
    permutations = []
    ArrayPermutation.permute_helper(input_array, permutations, 0)
    print(f"Generated permutations: {permutations}")
    assert len(permutations) == 6  # 3! combinaciones
    assert permutations == [
        [1, 2, 3], [1, 3, 2],
        [2, 1, 3], [2, 3, 1],
        [3, 1, 2], [3, 2, 1]
    ]