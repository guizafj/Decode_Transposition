from src.inputdata import InputData
from src.arraypermutation import ArrayPermutation
from src.decodification import Decodification
from src.myarrays import MyArrays
import sys

MAX_COMBINATIONS = 1000  # Límite máximo de combinaciones

class Main:
    """
    The Main class contains the main method that executes the program.
    This program deciphers an encrypted text using a transposition table
    and tests different permutations and configurations to find the original text.
    """

    @staticmethod
    def main():
        # Initialize user input
        input_data = InputData()
        cipher_text = input_data.cipher_text
        print(f"DECIPHERING...")
        print(f"Cipher text: {cipher_text}")
        print(f"Text length: {len(cipher_text)}")

        # Iterate over different column sizes
        for column_size in range(2, min(15, len(cipher_text))):  # Reducir el rango máximo de columnas
            print(f"Testing column size: {column_size}")
            
            # Calculate if this column size is viable
            rows = len(cipher_text) // column_size
            if len(cipher_text) % column_size > 0:
                rows += 1
            
            if rows * column_size > len(cipher_text) + column_size:
                print(f"Skipping column size {column_size} - would require too many characters")
                continue

            # Generate combinations and permutations
            overflows_list = ArrayPermutation.create_permutation_list_of_array_with_rep_items(
                MyArrays.create_space_array_of_length(len(cipher_text) % column_size, column_size)
            )
            permutation_list = ArrayPermutation.create_permutation_list_of_array_without_rep_items(
                MyArrays.create_of_length(column_size)
            )
            
            print(f"Column size: {column_size}, Permutations: {len(permutation_list)}, Overflows: {len(overflows_list)}")
            print(f"Processing column size: {column_size}")
            print(f"Number of permutations: {len(permutation_list)}, Number of overflows: {len(overflows_list)}")
            
            # Limitar combinaciones
            if len(overflows_list) > MAX_COMBINATIONS or len(permutation_list) > MAX_COMBINATIONS:
                print(f"Skipping column size {column_size} - too many combinations")
                continue

            # Procesar combinaciones
            for permutation in permutation_list[:MAX_COMBINATIONS]:  # Limitar permutaciones procesadas
                for overflows in overflows_list[:MAX_COMBINATIONS]:  # Limitar "overflows" procesados
                    try:
                        decoded_text = Decodification.decode(permutation, overflows, cipher_text)
                        expected_spaces = Main.generate_string_of_spaces(column_size - (len(cipher_text) % column_size))
                        if input_data.possible_word in decoded_text and decoded_text.endswith(expected_spaces):
                            print(f"Found valid decryption: {decoded_text}")
                            sys.exit(0)
                    except ValueError:
                        continue

        print("No valid decryption found.")

    @staticmethod
    def print_array_list(permutations):
        for permutation in permutations:
            print(permutation)

    @staticmethod
    def generate_string_of_spaces(num_spaces):
        return "-" * num_spaces