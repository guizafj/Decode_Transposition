"""
test_transposition.py
Tests unitarios para verificar el correcto funcionamiento del cifrado
y descifrado por transposición de columnas.

Ejecutar con: python test_transposition.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from decodification import encrypt, decrypt, try_all_keys
from arraypermutation import get_all_permutations
from myarrays import build_matrix


def test_permutations():
    """Verifica que se generan todas las permutaciones correctamente."""
    perms_2 = get_all_permutations(2)
    assert len(perms_2) == 2, f"Esperado 2, obtenido {len(perms_2)}"

    perms_3 = get_all_permutations(3)
    assert len(perms_3) == 6, f"Esperado 6, obtenido {len(perms_3)}"

    perms_4 = get_all_permutations(4)
    assert len(perms_4) == 24, f"Esperado 24, obtenido {len(perms_4)}"

    print("✓ test_permutations OK")


def test_build_matrix():
    """Verifica la construcción de la matriz."""
    matrix = build_matrix("HOLAMUNDO", 3)
    assert len(matrix) == 3, f"Esperado 3 filas, obtenido {len(matrix)}"
    assert len(matrix[0]) == 3, f"Esperado 3 cols, obtenido {len(matrix[0])}"
    assert matrix[0] == ['H', 'O', 'L']
    assert matrix[1] == ['A', 'M', 'U']
    assert matrix[2] == ['N', 'D', 'O']
    print("✓ test_build_matrix OK")


def test_encrypt_decrypt_roundtrip():
    """Verifica que cifrar y descifrar devuelve el texto original."""
    test_cases = [
        ("HOLAMUNDO", [2, 0, 1]),
        ("HELLOWORLD", [1, 0]),
        ("ATACARALBAMANECER", [3, 1, 2, 0]),
        ("SECRETO", [1, 0, 2]),
    ]

    for plaintext, key in test_cases:
        ciphertext = encrypt(plaintext, key)
        decrypted = decrypt(ciphertext, key)
        # Eliminamos el relleno 'X' al comparar
        decrypted_clean = decrypted.rstrip('X')
        assert decrypted_clean == plaintext, (
            f"Fallo con '{plaintext}' clave {key}: "
            f"cifrado='{ciphertext}', descifrado='{decrypted_clean}'"
        )

    print("✓ test_encrypt_decrypt_roundtrip OK")


def test_known_example():
    """
    Prueba con un ejemplo verificado:
    Cifrar HELLOWORLD con clave [0,1] produce HLOOLELWRD
    Luego descifrar con keyword HELLO debe recuperarlo.
    """
    # Primero ciframos para obtener un texto cifrado válido
    original = "HELLOWORLD"
    key = [1, 0]  # intercambiar columnas
    ciphertext = encrypt(original, key)
    print(f"  Cifrado de '{original}' con clave {key}: '{ciphertext}'")

    solutions = try_all_keys(ciphertext, len(key), "HELLO")
    assert len(solutions) > 0, "Debería encontrar al menos una solución"

    plaintexts = [s['plaintext'] for s in solutions]
    assert any("HELLO" in p for p in plaintexts), (
        f"Ningún texto descifrado contiene 'HELLO': {plaintexts}"
    )
    print(f"✓ test_known_example OK — Soluciones: {[s['plaintext'] for s in solutions]}")


def test_no_solution():
    """Verifica que se retorna lista vacía cuando no hay solución."""
    solutions = try_all_keys("XYZXYZXYZ", 3, "HELLO")
    assert solutions == [], f"Esperaba lista vacía, obtuvo {solutions}"
    print("✓ test_no_solution OK")


def test_spanish_attack():
    """
    Simula un ataque real en español:
    Mensaje: ATACARALBAMANECER
    Clave: [3, 1, 2, 0] (4 columnas)
    Palabra probable: ALBA
    """
    original = "ATACARALBAMANECER"
    key = [3, 1, 2, 0]

    ciphertext = encrypt(original, key)
    print(f"  Cifrado de '{original}' con clave {key}: '{ciphertext}'")

    solutions = try_all_keys(ciphertext, len(key), "ALBA")
    assert len(solutions) > 0, "Debería encontrar la solución"

    found_key = solutions[0]['key']
    assert found_key == key, f"Clave encontrada {found_key} != clave real {key}"
    print(f"✓ test_spanish_attack OK — Clave recuperada: {found_key}")


if __name__ == "__main__":
    print("═" * 50)
    print("   🧪 Ejecutando tests unitarios")
    print("═" * 50)

    tests = [
        test_permutations,
        test_build_matrix,
        test_encrypt_decrypt_roundtrip,
        test_known_example,
        test_no_solution,
        test_spanish_attack,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FALLIDO: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print("═" * 50)
    print(f"   Resultados: {passed} pasados, {failed} fallidos")
    print("═" * 50)
    sys.exit(0 if failed == 0 else 1)