"""
decodification.py
Lógica central para cifrar y descifrar por transposición de columnas.
"""

import math
from myarrays import build_matrix, read_by_columns, read_by_rows


def encrypt(plaintext: str, key: list[int]) -> str:
    """
    Cifra un texto usando transposición de columnas.

    El texto se escribe en una matriz de `len(key)` columnas (rellenando por
    filas) y luego se leen las columnas en el orden dado por `key`.

    Args:
        plaintext: Texto original (se convierte a mayúsculas, sin espacios).
        key: Permutación de índices 0..n-1 (ej: [2, 0, 1]).

    Returns:
        Texto cifrado.

    Ejemplo:
        encrypt("HOLAMUNDO", [2, 0, 1])
        Tabla:
            Col 0 1 2
                H O L
                A M U
                N D O
        Lectura en orden [2,0,1] → col2 + col0 + col1 = LUO + HAN + OMD
        → "LUOHANOMDT" (relleno con X si hace falta)
    """
    text = plaintext.upper().replace(" ", "")
    num_cols = len(key)
    matrix = build_matrix(text, num_cols)
    return read_by_columns(matrix, key)


def decrypt(ciphertext: str, key: list[int]) -> str:
    """
    Descifra un texto cifrado por transposición de columnas conociendo la clave.

    El proceso invierte el cifrado:
    1. Calcula cuántas filas tiene la matriz.
    2. Determina la longitud de cada columna (puede variar en la última fila).
    3. Reconstruye la matriz colocando el texto cifrado columna a columna
        según la clave inversa.
    4. Lee la matriz por filas para obtener el texto plano.

    Args:
        ciphertext: Texto cifrado.
        key: Permutación de índices 0..n-1 (misma que se usó para cifrar).

    Returns:
        Texto descifrado (puede tener 'X' de relleno al final).
    """
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)
    total_cells = num_rows * num_cols
    # Cuántas celdas de la última fila están "vacías" (fueron relleno)
    num_short_cols = total_cells - len(ciphertext)

    # Calculamos la longitud de cada columna en orden original (0..n-1)
    col_lengths = []
    for col in range(num_cols):
        # Las columnas cuyo índice original >= (num_cols - num_short_cols)
        # tienen una fila menos si aparecen al final de la clave
        # Más preciso: identificamos qué posición ocupa cada col en la clave
        position_in_key = key.index(col)
        if position_in_key >= (num_cols - num_short_cols):
            col_lengths.append(num_rows - 1)
        else:
            col_lengths.append(num_rows)

    # Construimos las columnas a partir del ciphertext
    columns = {}
    index = 0
    for key_pos, col in enumerate(key):
        length = col_lengths[col]
        columns[col] = list(ciphertext[index:index + length])
        index += length

    # Leemos por filas reconstruyendo el mensaje original
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(columns[col]):
                result.append(columns[col][row])

    return ''.join(result)


def try_all_keys(ciphertext: str, key_length: int, keyword: str) -> list[dict]:
    """
    Prueba todas las permutaciones de clave para una longitud dada y
    devuelve las soluciones que contienen la palabra clave.

    Args:
        ciphertext: Texto cifrado.
        key_length: Longitud de la clave a probar.
        keyword: Palabra que debe aparecer en el texto descifrado.

    Returns:
        Lista de diccionarios con 'key' y 'plaintext' de cada solución válida.
    """
    from arraypermutation import get_all_permutations

    solutions = []
    keyword_upper = keyword.upper()
    permutations_list = get_all_permutations(key_length)

    for key in permutations_list:
        plaintext = decrypt(ciphertext, key)
        if keyword_upper in plaintext:
            solutions.append({
                'key': key,
                'plaintext': plaintext
            })

    return solutions


def brute_force(ciphertext: str, keyword: str, max_key_length: int = 8) -> list[dict]:
    """
    Ataque de fuerza bruta probando todas las longitudes de clave posibles.

    ADVERTENCIA: Para key_length > 8 el número de permutaciones (8! = 40320)
    crece factorialmente. Con key_length=10 son 3.6 millones de intentos.

    Args:
        ciphertext: Texto cifrado.
        keyword: Palabra probable en el texto original.
        max_key_length: Longitud máxima de clave a probar (por defecto 8).

    Returns:
        Lista de todas las soluciones encontradas con su longitud de clave.
    """
    all_solutions = []
    for length in range(2, max_key_length + 1):
        solutions = try_all_keys(ciphertext, length, keyword)
        for sol in solutions:
            sol['key_length'] = length
            all_solutions.append(sol)
        if solutions:
            print(f"  ✓ Encontradas {len(solutions)} soluciones con clave de longitud {length}")
    return all_solutions