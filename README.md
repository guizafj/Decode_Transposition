# 🔐 Decode Transposition

**Decodificador y cifrador por transposición de columnas con clave**, desarrollado en Python como herramienta de aprendizaje en criptografía clásica y hacking ético.

Permite cifrar mensajes y descifrarlos tanto con clave conocida como sin ella, usando una **palabra probable** del texto original para realizar un ataque de fuerza bruta por permutaciones.

---

## 📚 Tabla de contenidos

- [¿Qué es el cifrado por transposición de columnas?](#-qué-es-el-cifrado-por-transposición-de-columnas)
- [¿Cómo funciona el cifrado?](#-cómo-funciona-el-cifrado)
- [¿Cómo funciona el descifrado?](#-cómo-funciona-el-descifrado)
- [El ataque por palabra probable](#-el-ataque-por-palabra-probable)
- [Instalación](#-instalación)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Uso interactivo](#-uso-interactivo)
- [Uso por terminal (línea de comandos)](#-uso-por-terminal-línea-de-comandos)
- [Referencia de argumentos](#-referencia-de-argumentos)
- [Licencia](#-licencia)

---

## 🧠 ¿Qué es el cifrado por transposición de columnas?

El **cifrado por transposición** es una técnica criptográfica clásica en la que las letras del mensaje original **no se sustituyen** (como en César o Vigenère), sino que se **reordenan** según una clave.

El resultado es un texto con las mismas letras del original, pero en un orden diferente que hace el mensaje ilegible sin conocer la clave.

> Es uno de los cifrados más estudiados en criptografía y sigue siendo relevante en CTFs (Capture The Flag) y análisis de seguridad.

---

## ✏️ ¿Cómo funciona el cifrado?

El proceso tiene tres pasos:

### Paso 1 — Escribir el mensaje en una tabla

Se escribe el texto plano en una tabla de izquierda a derecha y de arriba abajo. El número de columnas lo determina la longitud de la clave.

**Ejemplo:** mensaje `HOLAMUNDO`, clave `[2, 0, 1]` (3 columnas)

```
Índice columna →   0    1    2
                   H    O    L
                   A    M    U
                   N    D    O
```

> Si el mensaje no llena la última fila, se rellena con `X`.

### Paso 2 — Leer las columnas en el orden de la clave

La clave `[2, 0, 1]` indica el orden en que se leen las columnas:
primero la columna **2**, luego la **0**, luego la **1**.

```
Columna 2 → L U O
Columna 0 → H A N
Columna 1 → O M D
```

### Paso 3 — Concatenar

```
Texto cifrado: L U O H A N O M D  →  LUOHANOMD
```

---

## 🔓 ¿Cómo funciona el descifrado?

El descifrado invierte el proceso. Para ello se necesita conocer la clave.

### Paso 1 — Calcular el tamaño de la tabla

Con la longitud del texto cifrado y la longitud de la clave se sabe cuántas filas tiene la tabla original.

```
len("LUOHANOMD") = 9   |   columnas = 3   →   filas = 9 / 3 = 3
```

### Paso 2 — Reconstruir las columnas

Se distribuye el texto cifrado en columnas **siguiendo el orden de la clave**:

```
Clave [2, 0, 1]:
  La primera porción del cifrado va a la columna 2 → L U O
  La segunda porción va a la columna 0             → H A N
  La tercera porción va a la columna 1             → O M D
```

### Paso 3 — Leer por filas

Una vez reconstruida la tabla, se lee fila por fila:

```
Fila 0: H O L
Fila 1: A M U
Fila 2: N D O

Resultado: HOLAMUNDO ✓
```

---

## 🕵️ El ataque por palabra probable

En escenarios reales de criptoanálisis muchas veces **no se conoce la clave**, pero sí se puede intuir una palabra que probablemente aparezca en el mensaje original (por ejemplo: `ATACAR`, `SECRETO`, `HOLA`, etc.).

Este tipo de ataque se llama **known-plaintext attack** (ataque de texto en claro conocido).

### ¿Cómo funciona el ataque?

El programa genera **todas las permutaciones posibles** de una clave de longitud N y descifra el texto con cada una. Si el resultado contiene la palabra probable, esa clave es una solución candidata.

### Complejidad del ataque (número de intentos)

El número de permutaciones crece **factorialmente** con la longitud de la clave:

| Longitud de clave | Permutaciones posibles |
|:-----------------:|:---------------------:|
| 2                 | 2! = **2**            |
| 3                 | 3! = **6**            |
| 4                 | 4! = **24**           |
| 5                 | 5! = **120**          |
| 6                 | 6! = **720**          |
| 7                 | 7! = **5,040**        |
| 8                 | 8! = **40,320**       |
| 10                | 10! = **3,628,800**   |

> Para longitudes de clave mayores a 10 el tiempo de cómputo puede ser considerable.
> Se recomienda usar `--max-length 8` como límite por defecto.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/guizafj/Decode_Transposition.git
cd Decode_Transposition
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

> El proyecto usa únicamente la librería estándar de Python 3.10+.
> `requirements.txt` está incluido para compatibilidad futura.

---

## 📁 Estructura del proyecto

```
Decode_Transposition/
├── src/
│   ├── __init__.py           # Exporta las funciones principales del paquete
│   ├── arraypermutation.py   # Genera todas las permutaciones de índices
│   ├── myarrays.py           # Construye y lee la matriz de transposición
│   ├── decodification.py     # Lógica central: cifrar, descifrar, atacar
│   ├── inputdata.py          # Parseo y validación de argumentos CLI
│   └── main.py               # Punto de entrada (interactivo + CLI)
├── test_transposition.py     # Suite de tests unitarios
├── requirements.txt
├── README.md
└── LICENSE
```

| Archivo | Responsabilidad |
|---|---|
| `arraypermutation.py` | Usa `itertools.permutations` para generar todas las permutaciones de `[0..n-1]` |
| `myarrays.py` | `build_matrix()` construye la tabla; `read_by_columns()` cifra; `read_by_rows()` descifra |
| `decodification.py` | Orquesta `encrypt()`, `decrypt()`, `try_all_keys()` y `brute_force()` |
| `inputdata.py` | Define y valida los argumentos `--ciphertext`, `--keyword`, `--key`, etc. |
| `main.py` | Detecta si hay argumentos CLI; si no, lanza el menú interactivo |

---

## 💬 Uso interactivo

El modo interactivo es ideal para aprender o usar la herramienta sin recordar los argumentos.
Se activa ejecutando el script **sin ningún argumento**:

```bash
python src/main.py
```

Verás el siguiente menú:

```
╔══════════════════════════════════════════════════════╗
║   🔐 Decode Transposition — Cifrado por Columnas    ║
║      Herramienta para ciberseguridad y CTF          ║
╚══════════════════════════════════════════════════════╝

¿Qué deseas hacer?

  [1] Cifrar un mensaje
  [2] Descifrar con clave conocida
  [3] Descifrar con palabra probable (ataque por permutaciones)
  [4] Fuerza bruta (probar todas las longitudes de clave)
  [0] Salir
```

### Opción 1 — Cifrar un mensaje

El programa te pide el texto, el número de columnas y la clave:

```
── MODO CIFRADO ──────────────────────────────────────
  Texto a cifrar: HOLAMUNDO
  Número de columnas (longitud de la clave, ej: 3): 3
  Ingresa la clave (3 índices de 0 a 2, separados por espacios)
  Ejemplo: [2, 1, 0]
  > 2 0 1

  📝 Texto original : HOLAMUNDO
  🔑 Clave usada    : [2, 0, 1]  (base 0)
  🔒 Texto cifrado  : LUOHANOMD
```

> **Nota sobre la clave:** se usan índices en **base 0**. Para 3 columnas, los índices son `0`, `1` y `2`. La clave `2 0 1` significa: "lee primero la columna 2, luego la 0, luego la 1".

### Opción 2 — Descifrar con clave conocida

Úsala cuando conoces exactamente la clave que se usó para cifrar:

```
── DESCIFRADO CON CLAVE CONOCIDA ─────────────────────
  Texto cifrado: LUOHANOMD
  ¿Cuántas columnas tiene la clave?: 3
  Ingresa la clave (3 índices de 0 a 2):
  > 2 0 1

  🔒 Texto cifrado   : LUOHANOMD
  🔑 Clave usada     : [2, 0, 1]  (base 0)
  🔓 Texto descifrado: HOLAMUNDO
```

### Opción 3 — Descifrar con palabra probable

Úsala cuando **no conoces la clave** pero sabes (o sospechas) una palabra del mensaje original:

```
── DESCIFRADO POR PALABRA PROBABLE ───────────────────
  Texto cifrado: LUOHANOMD
  Palabra probable en el texto original: HOLA
  Longitud de clave a probar: 3

  🔍 Probando 3! = 6 permutaciones...

  ✅ Se encontraron 1 solución(es):
  ────────────────────────────────────────────────────
  Solución #1
    Clave (base 1, más intuitiva): [3, 1, 2]
    Clave (base 0, para el código): [2, 0, 1]
    Texto descifrado: HOLAMUNDO
  ────────────────────────────────────────────────────
  ⏱️  Tiempo: 0.001s
```

### Opción 4 — Fuerza bruta

Prueba **todas las longitudes de clave** desde 2 hasta el máximo que indiques.
Ideal cuando ni siquiera sabes cuántas columnas tiene la clave:

```
── FUERZA BRUTA ──────────────────────────────────────
  Texto cifrado: LUOHANOMD
  Palabra probable en el texto original: HOLA
  Longitud máxima de clave a probar (recomendado ≤ 8): 5

  💪 Iniciando fuerza bruta (152 intentos en total)...
    ✓ Encontradas 1 soluciones con clave de longitud 3

  ✅ Se encontraron 1 solución(es):
  ────────────────────────────────────────────────────
  Solución #1
    Clave (base 0): [2, 0, 1]
    Texto descifrado: HOLAMUNDO
    Longitud de clave: 3
  ────────────────────────────────────────────────────
```

---

## 💻 Uso por terminal (línea de comandos)

El modo CLI es ideal para automatización, scripts y flujos de trabajo en CTFs.
Se activa pasando al menos un argumento al ejecutar el script.

### Cifrar un mensaje

```bash
python src/main.py --encrypt --plaintext "HOLAMUNDO" --key 2 0 1
```

Salida:
```
  📝 Texto plano   : HOLAMUNDO
  🔑 Clave (base 0): [2, 0, 1]
  🔒 Texto cifrado : LUOHANOMD
```

### Descifrar con clave conocida

```bash
python src/main.py --ciphertext "LUOHANOMD" --key 2 0 1
```

### Descifrar con palabra probable (longitud de clave conocida)

```bash
python src/main.py --ciphertext "LUOHANOMD" --keyword "HOLA" --key-length 3
```

### Fuerza bruta (longitud de clave desconocida)

```bash
python src/main.py --ciphertext "LUOHANOMD" --keyword "HOLA" --brute-force
```

### Fuerza bruta con límite de longitud personalizado

```bash
python src/main.py --ciphertext "LUOHANOMD" --keyword "HOLA" --brute-force --max-length 10
```

### Versiones cortas de los argumentos

Todos los argumentos tienen una versión abreviada:

```bash
python src/main.py -c "LUOHANOMD" -k "HOLA" -l 3
#                   ↑               ↑         ↑
#             --ciphertext     --keyword  --key-length
```

---

## 📋 Referencia de argumentos

| Argumento largo | Corto | Tipo | Descripción |
|---|---|---|---|
| `--encrypt` | `-e` | flag | Activa el modo cifrado |
| `--brute-force` | `-b` | flag | Activa el modo fuerza bruta |
| `--plaintext` | `-p` | texto | Texto plano a cifrar (requiere `--encrypt`) |
| `--ciphertext` | `-c` | texto | Texto cifrado a descifrar |
| `--keyword` | `-k` | texto | Palabra probable en el texto original |
| `--key` | — | enteros | Clave explícita como lista de índices (ej: `--key 2 0 1`) |
| `--key-length` | `-l` | entero | Longitud de clave para ataque por permutaciones |
| `--max-length` | `-m` | entero | Longitud máxima para fuerza bruta (default: `8`) |

### Combinaciones válidas

| Objetivo | Argumentos requeridos |
|---|---|
| Cifrar | `--encrypt` + `--plaintext` + `--key` |
| Descifrar con clave | `--ciphertext` + `--key` |
| Atacar con keyword | `--ciphertext` + `--keyword` + `--key-length` |
| Fuerza bruta | `--brute-force` + `--ciphertext` + `--keyword` |

---

## 🧪 Ejecutar los tests

```bash
python test_transposition.py
```

Salida esperada:

```
══════════════════════════════════════════
   🧪 Ejecutando tests unitarios
══════════════════════════════════════════
✓ test_permutations OK
✓ test_build_matrix OK
✓ test_encrypt_decrypt_roundtrip OK
✓ test_known_example OK
✓ test_no_solution OK
✓ test_spanish_attack OK
══════════════════════════════════════════
   Resultados: 6 pasados, 0 fallidos
══════════════════════════════════════════
```

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, no dudes en abrir un issue o realizar un pull request.

---

## 📬 Contacto

Para consultas o sugerencias: [contacto@dguiza.dev](mailto:contacto@dguiza.dev)