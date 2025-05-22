# 🔐 Decode\_Transposition

**Decodificador de cifrado por transposición de columnas con clave**, utilizando una palabra probable para facilitar el descifrado.

Este proyecto permite descifrar mensajes cifrados mediante transposición de columnas, una técnica clásica de criptografía. Al proporcionar una palabra probable que pueda aparecer en el texto original, el programa intenta reconstruir el mensaje original sin necesidad de conocer la clave exacta.

---

## 🧠 ¿Cómo funciona?

El cifrado por transposición de columnas reorganiza las letras del mensaje original según una clave específica, sin alterar las letras en sí. Este decodificador:

1. **Recibe** el texto cifrado y una palabra probable que se espera encontrar en el mensaje original.
2. **Genera** todas las permutaciones posibles de claves de longitud determinada.
3. **Aplica** cada clave para descifrar el mensaje.
4. **Verifica** si la palabra probable aparece en el texto descifrado.
5. **Devuelve** las posibles soluciones que contienen la palabra probable.

---

## 🚀 Instalación

1. **Clona** el repositorio:

   ```bash
   git clone https://github.com/guizafj/Decode_Transposition.git
   cd Decode_Transposition
   ```

2. **Instala** las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Uso

Ejecuta el script principal proporcionando el texto cifrado y la palabra probable:

```bash
python src/decode_transposition.py --ciphertext "TextoCifrado" --keyword "palabra"
```

Parámetros:

* `--ciphertext`: Texto cifrado que deseas descifrar.
* `--keyword`: Palabra que se espera encontrar en el mensaje original.

Ejemplo:

```bash
python src/decode_transposition.py --ciphertext "HLOELWRDLO" --keyword "HELLO"
```

---

## 📁 Estructura del proyecto

```
Decode_Transposition/
├── src/
│   └── __init__.py
│   └── arraypermutation.py
│   └── decodification.py
│   └── inputdata.py
│   └── main.py
│   └── myarrays.py
├── requirements.txt
├── README.md
└── LICENSE
```

* `src/main.py`: Script principal que realiza el descifrado.
* `requirements.txt`: Lista de dependencias necesarias.
* `README.md`: Documentación del proyecto.
* `LICENSE`: Licencia del proyecto (MIT).

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, no dudes en abrir un issue o realizar un pull request.

---

## 📬 Contacto

Para consultas o sugerencias, puedes contactarme a través de contacto@dguiza.dev