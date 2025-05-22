from src.decodification import Decodification

def test_rows_calculator():
    assert Decodification.rows_calculator("HELLO", 3) == 2
    assert Decodification.rows_calculator("HELLO", 5) == 1

def test_key_transformation():
    key = "CAB"
    transformed_key = Decodification.key_transformation(key)
    assert transformed_key == [2, 0, 1]  # Example transformation based on alphabetical order.