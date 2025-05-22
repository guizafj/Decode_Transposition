from src.myarrays import MyArrays

def test_create_of_length():
    result = MyArrays.create_of_length(5)
    assert result == [0, 1, 2, 3, 4]  # Verifica que la lista generada sea correcta.

def test_create_space_array_of_length():
    result = MyArrays.create_space_array_of_length(3, 5)
    assert result == [1, 1, 1, 0, 0]  # Verifica que las primeras 3 posiciones sean `1` y el resto `0`.

    result = MyArrays.create_space_array_of_length(6, 5)
    assert result == []  # Verifica que se retorne una lista vacía si `spaces` > `length`.