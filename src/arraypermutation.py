from itertools import product

class ArrayPermutation:

    @staticmethod
    def create_permutation_list_of_array_with_rep_items(input_array):
        """
        Generate permutations with repetition, ensuring the input array is sorted first.
        """
        # Ordenar el arreglo de entrada para garantizar un orden consistente
        input_array.sort()

        """"
        Generate permutations with repetition.
        """
        from itertools import product
        return [list(p) for p in product(input_array, repeat=len(input_array))]


    @staticmethod
    def create_permutation_list_of_array_without_rep_items(input_array):
        permutation_lists = []
        ArrayPermutation.permute_helper(input_array, permutation_lists, 0)  # Generate permutations without repetition recursively.
        return permutation_lists

    @staticmethod
    def permute_helper(input_array, permutation_lists, current_index):
        """
        Generate permutations without repetition recursively.
        """
        if current_index == len(input_array):
            permutation_lists.append(input_array[:])
            return

        for i in range(current_index, len(input_array)):
            input_array[current_index], input_array[i] = input_array[i], input_array[current_index]
            ArrayPermutation.permute_helper(input_array, permutation_lists, current_index + 1)
            input_array[current_index], input_array[i] = input_array[i], input_array[current_index]

    @staticmethod
    def permute_rep_iterative(input_array, permutation_lists):
        """
        Generate permutations with repetition iteratively.
        """
        from itertools import product
        for p in product(input_array, repeat=len(input_array)):
            permutation_lists.append(list(p))