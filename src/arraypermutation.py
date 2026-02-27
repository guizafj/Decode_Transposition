"""
arraypermutation.py
Genera todas las permutaciones posibles de una lista de índices.
"""

from itertools import permutations


def get_all_permutations(n: int) -> list[list[int]]:
    """
    Genera todas las permutaciones de los índices [0, 1, ..., n-1].

    Args:
        n: Longitud de la clave (número de columnas).

    Returns:
        Lista de listas, donde cada sublista es una permutación de índices.
    """
    indices = list(range(n))
    return [list(p) for p in permutations(indices)]


if __name__ == "__main__":
    # Prueba rápida
    perms = get_all_permutations(3)
    print(f"Permutaciones para n=3: {len(perms)}")
    for p in perms:
        print(p)