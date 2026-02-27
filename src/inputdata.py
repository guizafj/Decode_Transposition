"""
inputdata.py
Manejo de argumentos de línea de comandos y validación de entrada.
"""

import argparse
import sys


def parse_arguments() -> argparse.Namespace:
    """
    Define y parsea los argumentos de línea de comandos.

    Returns:
        Namespace con los argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        prog="decode_transposition",
        description=(
            "🔐 Decodificador de cifrado por transposición de columnas.\n"
            "Dado un texto cifrado y una palabra probable, intenta encontrar\n"
            "la clave probando todas las permutaciones posibles."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python main.py -c 'OMDLUHANO' -k 'HOLA' -l 3\n"
            "  python main.py -c 'HLOELWRDLO' -k 'HELLO' --brute-force\n"
            "  python main.py --encrypt -p 'HOLAMUNDO' --key 2 0 1\n"
        )
    )

    # Modo de operación
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--encrypt', '-e',
        action='store_true',
        help='Modo cifrado: cifra el texto plano con la clave dada.'
    )
    mode_group.add_argument(
        '--brute-force', '-b',
        action='store_true',
        help='Fuerza bruta: prueba todas las longitudes de clave hasta --max-length.'
    )

    # Argumentos principales
    parser.add_argument(
        '--ciphertext', '-c',
        type=str,
        help='Texto cifrado a descifrar.'
    )
    parser.add_argument(
        '--plaintext', '-p',
        type=str,
        help='Texto plano a cifrar (requiere --encrypt).'
    )
    parser.add_argument(
        '--keyword', '-k',
        type=str,
        help='Palabra probable que debería aparecer en el texto descifrado.'
    )
    parser.add_argument(
        '--key-length', '-l',
        type=int,
        help='Longitud de la clave a probar (número de columnas).'
    )
    parser.add_argument(
        '--key',
        type=int,
        nargs='+',
        help='Clave explícita como lista de índices (ej: --key 2 0 1).'
    )
    parser.add_argument(
        '--max-length', '-m',
        type=int,
        default=8,
        help='Longitud máxima de clave para fuerza bruta (default: 8).'
    )

    args = parser.parse_args()
    validate_arguments(parser, args)
    return args


def validate_arguments(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Valida combinaciones de argumentos."""
    if args.encrypt:
        if not args.plaintext:
            parser.error("--encrypt requiere --plaintext/-p")
        if not args.key:
            parser.error("--encrypt requiere --key")
    elif args.brute_force:
        if not args.ciphertext:
            parser.error("--brute-force requiere --ciphertext/-c")
        if not args.keyword:
            parser.error("--brute-force requiere --keyword/-k")
    else:
        # Modo descifrado por defecto
        if not args.ciphertext:
            parser.error("Se requiere --ciphertext/-c para descifrar")
        if not args.keyword and not args.key:
            parser.error("Se requiere --keyword/-k o --key para descifrar")
        if not args.key_length and not args.key:
            parser.error("Se requiere --key-length/-l o --key para descifrar")