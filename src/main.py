"""
main.py
Script principal del decodificador por transposición de columnas.

Modos de uso:
    1. Interactivo (sin argumentos):
        python main.py

    2. Línea de comandos:
        python main.py --ciphertext "TEXTO"  --keyword "PALABRA" --key-length 3
        python main.py --encrypt --plaintext "HOLAMUNDO" --key 2 0 1
        python main.py --ciphertext "TEXTO"  --keyword "PALABRA" --brute-force
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inputdata import parse_arguments
from decodification import encrypt, decrypt, try_all_keys, brute_force


BANNER = r"""
╔══════════════════════════════════════════════════════╗
║   🔐 Decode Transposition — Cifrado por Columnas    ║
║      Herramienta para ciberseguridad y CTF          ║
╚══════════════════════════════════════════════════════╝
"""

MENU = """
¿Qué deseas hacer?

    [1] Cifrar un mensaje
    [2] Descifrar con clave conocida
    [3] Descifrar con palabra probable (ataque por permutaciones)
    [4] Fuerza bruta (probar todas las longitudes de clave)
    [0] Salir
"""

SEP = "─" * 60


# ─────────────────────────────────────────────
#  Helpers de entrada interactiva
# ─────────────────────────────────────────────

def ask(prompt: str, required: bool = True) -> str:
    """Lee una línea de texto desde la consola, validando que no esté vacía."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if not required:
            return ""
        print("  ⚠  El campo no puede estar vacío. Intenta de nuevo.")


def ask_int(prompt: str, min_val: int = 1, max_val: int = 999) -> int:
    """Lee un entero dentro de un rango."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_val <= value <= max_val:
                return value
            print(f"  ⚠  Ingresa un número entre {min_val} y {max_val}.")
        except ValueError:
            print("  ⚠  Eso no es un número válido. Intenta de nuevo.")


def ask_key(num_cols: int) -> list[int]:
    """
    Solicita una clave como lista de números separados por espacios.
    Ejemplo: '2 0 1' → [2, 0, 1]

    Valida que:
    - Sean exactamente `num_cols` números.
    - Formen una permutación válida de 0..num_cols-1.
    """
    while True:
        raw = input(f"  Ingresa la clave ({num_cols} índices de 0 a {num_cols-1}, "
                    f"separados por espacios)\n  Ejemplo: {list(range(num_cols-1, -1, -1))}\n  > ").strip()
        try:
            parts = list(map(int, raw.split()))
            if len(parts) != num_cols:
                print(f"  ⚠  Se esperan {num_cols} números, ingresaste {len(parts)}.")
                continue
            if sorted(parts) != list(range(num_cols)):
                print(f"  ⚠  Deben ser una permutación de {list(range(num_cols))} (sin repetir).")
                continue
            return parts
        except ValueError:
            print("  ⚠  Ingresa solo números enteros separados por espacios.")


# ─────────────────────────────────────────────
#  Lógica de presentación (compartida)
# ─────────────────────────────────────────────

def display_solutions(solutions: list[dict]) -> None:
    """Muestra las soluciones encontradas de forma legible."""
    if not solutions:
        print("\n❌ No se encontraron soluciones con la palabra clave dada.")
        print("   Sugerencias:")
        print("   • Prueba con otra palabra probable")
        print("   • Verifica que el texto cifrado sea correcto")
        print("   • Usa fuerza bruta para probar más longitudes de clave")
        return

    print(f"\n✅ Se encontraron {len(solutions)} solución(es):\n")
    print(SEP)
    for i, sol in enumerate(solutions, 1):
        key_display = [k + 1 for k in sol['key']]
        print(f"Solución #{i}")
        print(f"  Clave (base 1, más intuitiva): {key_display}")
        print(f"  Clave (base 0, para el código): {sol['key']}")
        print(f"  Texto descifrado: {sol['plaintext']}")
        if 'key_length' in sol:
            print(f"  Longitud de clave: {sol['key_length']}")
        print(SEP)


# ─────────────────────────────────────────────
#  Flujos interactivos
# ─────────────────────────────────────────────

def interactive_encrypt() -> None:
    print("\n── MODO CIFRADO ──────────────────────────────────────")
    plaintext = ask("  Texto a cifrar: ")
    num_cols  = ask_int("  Número de columnas (longitud de la clave, ej: 3): ",
                        min_val=2, max_val=20)
    key = ask_key(num_cols)

    text = plaintext.upper().replace(" ", "")
    ciphertext = encrypt(text, key)

    print()
    print(f"  📝 Texto original : {plaintext}")
    print(f"  🔑 Clave usada    : {key}  (base 0)")
    print(f"  🔒 Texto cifrado  : {ciphertext}")


def interactive_decrypt_known_key() -> None:
    print("\n── DESCIFRADO CON CLAVE CONOCIDA ─────────────────────")
    ciphertext = ask("  Texto cifrado: ").upper()
    num_cols   = ask_int("  ¿Cuántas columnas tiene la clave?: ", min_val=2, max_val=20)
    key        = ask_key(num_cols)

    plaintext = decrypt(ciphertext, key)

    print()
    print(f"  🔒 Texto cifrado  : {ciphertext}")
    print(f"  🔑 Clave usada    : {key}  (base 0)")
    print(f"  🔓 Texto descifrado: {plaintext}")


def interactive_decrypt_keyword() -> None:
    print("\n── DESCIFRADO POR PALABRA PROBABLE ───────────────────")
    print("  (Útil cuando conoces una palabra que debería aparecer")
    print("   en el mensaje original, pero NO conoces la clave)\n")
    ciphertext  = ask("  Texto cifrado: ").upper()
    keyword     = ask("  Palabra probable en el texto original: ").upper()
    key_length  = ask_int("  Longitud de clave a probar (número de columnas): ",
                        min_val=2, max_val=12)

    print(f"\n  🔍 Probando {key_length}! = ", end="")
    from math import factorial
    print(f"{factorial(key_length):,} permutaciones...")

    start     = time.time()
    solutions = try_all_keys(ciphertext, key_length, keyword)
    elapsed   = time.time() - start

    display_solutions(solutions)
    print(f"\n  ⏱️  Tiempo: {elapsed:.3f}s")


def interactive_brute_force() -> None:
    print("\n── FUERZA BRUTA ──────────────────────────────────────")
    print("  (Prueba todas las longitudes de clave de 2 hasta N)\n")
    ciphertext  = ask("  Texto cifrado: ").upper()
    keyword     = ask("  Palabra probable en el texto original: ").upper()
    max_length  = ask_int("  Longitud máxima de clave a probar (recomendado ≤ 8): ",
                        min_val=2, max_val=12)

    from math import factorial
    total = sum(factorial(n) for n in range(2, max_length + 1))
    print(f"\n  💪 Iniciando fuerza bruta ({total:,} intentos en total)...")

    start     = time.time()
    solutions = brute_force(ciphertext, keyword, max_length)
    elapsed   = time.time() - start

    display_solutions(solutions)
    print(f"\n  ⏱️  Tiempo total: {elapsed:.3f}s")


# ─────────────────────────────────────────────
#  Flujos para modo línea de comandos
# ─────────────────────────────────────────────

def run_encrypt_mode(args) -> None:
    text = args.plaintext.upper().replace(" ", "")
    ciphertext = encrypt(text, args.key)
    print(f"\n  📝 Texto plano   : {args.plaintext}")
    print(f"  🔑 Clave (base 0): {args.key}")
    print(f"  🔒 Texto cifrado : {ciphertext}")


def run_decrypt_mode(args) -> None:
    ciphertext = args.ciphertext.upper()
    if args.key:
        plaintext = decrypt(ciphertext, args.key)
        print(f"\n  🔒 Texto cifrado   : {ciphertext}")
        print(f"  🔑 Clave (base 0)  : {args.key}")
        print(f"  🔓 Texto descifrado: {plaintext}")
    else:
        print(f"\n  🔍 Probando permutaciones de longitud {args.key_length}...")
        start = time.time()
        solutions = try_all_keys(ciphertext, args.key_length, args.keyword)
        elapsed = time.time() - start
        display_solutions(solutions)
        print(f"\n  ⏱️  Tiempo: {elapsed:.3f}s")


def run_brute_force_mode(args) -> None:
    from math import factorial
    ciphertext = args.ciphertext.upper()
    total = sum(factorial(n) for n in range(2, args.max_length + 1))
    print(f"\n  💪 Fuerza bruta ({total:,} intentos)...")
    start = time.time()
    solutions = brute_force(ciphertext, args.keyword, args.max_length)
    elapsed = time.time() - start
    display_solutions(solutions)
    print(f"\n  ⏱️  Tiempo total: {elapsed:.3f}s")


# ─────────────────────────────────────────────
#  Menú interactivo principal
# ─────────────────────────────────────────────

def run_interactive() -> None:
    """Bucle principal del modo interactivo."""
    actions = {
        "1": interactive_encrypt,
        "2": interactive_decrypt_known_key,
        "3": interactive_decrypt_keyword,
        "4": interactive_brute_force,
    }

    while True:
        print(MENU)
        choice = input("  Elige una opción [0-4]: ").strip()

        if choice == "0":
            print("\n  👋 Hasta luego.\n")
            break
        elif choice in actions:
            try:
                actions[choice]()
            except KeyboardInterrupt:
                print("\n  (operación cancelada)")
            input("\n  Presiona Enter para volver al menú...")
        else:
            print("  ⚠  Opción no válida. Elige entre 0 y 4.")


# ─────────────────────────────────────────────
#  Punto de entrada
# ─────────────────────────────────────────────

def main() -> None:
    print(BANNER)

    # Si el usuario ejecuta `python main.py` sin argumentos → modo interactivo
    if len(sys.argv) == 1:
        run_interactive()
        return

    # Si hay argumentos → modo línea de comandos (comportamiento original)
    args = parse_arguments()
    if args.encrypt:
        run_encrypt_mode(args)
    elif args.brute_force:
        run_brute_force_mode(args)
    else:
        run_decrypt_mode(args)


if __name__ == "__main__":
    main()