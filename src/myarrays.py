"""
myarrays.py
Utilidades para manipular listas/matrices usadas en la transposición.
"""

import math


def build_matrix(text: str, num_cols: int) -> list[list[str]]:
    """
    Construye una matriz de caracteres rellenando por filas.
    Si el texto no llena la última fila, rellena con 'X'.

    Args:
        text: Texto (cifrado o plano) a colocar en la matriz.
        num_cols: Número de columnas (= longitud de la clave).

    Returns:
        Matriz (lista de listas) de caracteres.
    """
    num_rows = math.ceil(len(text) / num_cols)
    # Rellenamos el texto si no es múltiplo de num_cols
    padded = text.ljust(num_rows * num_cols, 'X')

    matrix = []
    for row in range(num_rows):
        matrix.append(list(padded[row * num_cols:(row + 1) * num_cols]))
    return matrix


def read_by_columns(matrix: list[list[str]], key: list[int]) -> str:
    """
    Lee la matriz columna a columna en el orden indicado por la clave.
    Usado para CIFRAR.

    Args:
        matrix: Matriz de caracteres.
        key: Orden de lectura de columnas (ej: [2, 0, 1]).

    Returns:
        Texto cifrado.
    """
    result = []
    for col_index in key:
        for row in matrix:
            result.append(row[col_index])
    return ''.join(result)


def read_by_rows(matrix: list[list[str]]) -> str:
    """
    Lee la matriz fila por fila.
    Usado para obtener el texto plano después de reordenar columnas.

    Args:
        matrix: Matriz con columnas ya reordenadas.

    Returns:
        Texto plano.
    """
    result = []
    for row in matrix:
        result.extend(row)
    return ''.join(result)


def print_matrix(matrix: list[list[str]], key: list[int] = None) -> None:
    """Imprime la matriz con encabezados opcionales de clave."""
    if key:
        print("  ".join(str(k) for k in key))
        print("  ".join("-" for _ in key))
    for row in matrix:
        print("  ".join(row))
    print()