class MyArrays: 

    """
    La clase MyArrays proporciona métodos utilitarios para crear arreglos
    con valores específicos. Estos métodos son utilizados en la lógica de
    descifrado para generar arreglos necesarios en el proceso.
    """

    @staticmethod
    def create_of_length(length):
        array = [0] * length  # Inicializa un arreglo de la longitud especificada.
        for index in range(len(array)):
            array[index] = index  # Asigna el índice actual como valor en cada posición.
        return array  # Retorna el arreglo generado.

    @staticmethod
    def create_space_array_of_length(spaces, length):
        array = [0] * length  # Inicializa un arreglo de la longitud especificada.
        if spaces > length:
            return []  # Retorna un arreglo vacío si `spaces` es mayor que `length`.
        if not isinstance(spaces, int) or not isinstance(length, int) or spaces < 0 or length < 0:
            raise ValueError("Spaces and length must be non-negative integers.")
        for index in range(spaces):
            array[index] = 1  # Asigna el valor `1` a las primeras `spaces` posiciones.
        return array  # Retorna el arreglo generado.