class Decodification:

    @staticmethod
    def print_table(column_array, key):
        result = ""
        # Iterates over each row of the table.
        for column_array_row in column_array:
            # Traverses the columns in the order defined by the key.
            for i in range(len(column_array_row)):
                result += column_array_row[key[i]]  # Adds the corresponding character to the result.
        return result

    @staticmethod
    def decode(permutation, overflows, text):
        if not text:
            raise ValueError("The encrypted text cannot be empty.")

        # Calculate rows needed
        rows = Decodification.rows_calculator(text, len(permutation))

        # Create table with exact size needed
        table = [[''] * len(permutation) for _ in range(rows)]

        # Fill table
        text_pointer = 0
        for i in range(len(permutation)):
            for j in range(rows):
                if overflows[i] == 0 and j == rows - 1:
                    table[j][i] = '-'
                elif text_pointer < len(text):
                    table[j][i] = text[text_pointer]
                    text_pointer += 1
                else:
                    table[j][i] = '-'

        return Decodification.print_table(table, permutation)

    @staticmethod
    def rows_calculator(text, columns):
        # Calculate rows needed, rounding up
        rows = (len(text) + columns - 1) // columns
        
        # Validate that we won't need more characters than available
        required_length = rows * columns
        if required_length > len(text) + columns:
            raise ValueError(f"Invalid column size {columns} for text length {len(text)}")
        
        return rows

    @staticmethod
    def decode_with_brute_force():
        return None

    @staticmethod
    def key_transformation(key):
        transformation = []
        result = []
        key_to_upper = key.upper()  # Converts the key to uppercase.

        # Converts each character of the key into a numeric value based on its position in the alphabet.
        for char in key_to_upper:
            transformation.append(ord(char) - 64)  # 'A' = 1, 'B' = 2, etc.

        result = transformation.copy()  # Clones the transformation list.

        # Calculates the order of the columns based on the values of the key.
        for i in range(len(key)):
            position = Decodification.max_value(transformation)  # Finds the position of the maximum value.
            transformation[position] = 0  # Marks the value as processed.
            result[position] = len(key) - (i + 1)  # Assigns the inverse order.
        return result

    @staticmethod
    def max_value(transformation):
        pointer = 0
        # Iterates over the list to find the index of the maximum value.
        for i in range(len(transformation) - 1, 0, -1):
            if transformation[i] > transformation[pointer]:
                pointer = i
        return pointer

    @staticmethod
    def decode_with_brute_force(cipher_text):
        max_columns = len(cipher_text)
        print(f"Max columns: {max_columns}")
        # Tests all possible column sizes
        for column_size in range(1, max_columns + 1):
            rows = Decodification.rows_calculator(cipher_text, column_size)
            print(f"Trying column size {column_size} - {rows} rows")
            overflows = [0] * column_size  # Resets the overflows for the new column size

            # Adjusts the last row's overflow based on the remaining characters
            if len(cipher_text) % column_size != 0:
                overflows[-1] = len(cipher_text) % column_size

            # Skips the decoding if the calculated rows exceed the available characters
            if rows * column_size > len(cipher_text) + column_size:
                print(f"Skipping column size {column_size} - would require too many characters")
                continue

            permutation = Decodification.key_transformation(''.join([chr(65 + i) for i in range(column_size)]))
            decoded_text = Decodification.decode(permutation, overflows, cipher_text)
            print(f"Decoded text with column size {column_size}: {decoded_text}")