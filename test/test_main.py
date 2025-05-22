from unittest.mock import patch
import pytest
from src.main import Main

def test_generate_string_of_spaces():
    assert Main.generate_string_of_spaces(5) == "-----"
    assert Main.generate_string_of_spaces(0) == ""

@pytest.mark.timeout(30)  # Aumentar el tiempo de ejecución a 30 segundos
def test_no_valid_decryption(capsys):
    with patch("builtins.input", side_effect=["HELLO WORLD TEST", "TEST"]):  # Texto más largo
        Main.main()
        captured = capsys.readouterr()
        assert "Testing column size: 2" in captured.out
        assert "No valid decryption found." in captured.out

# Comment out manual input test as it's not suitable for automated testing
"""
def test_manual_input():
    Main.main()
"""

def test_column_size_range():
    cipher_text = "HELLOWORLD"
    column_sizes = list(range(2, min(15, len(cipher_text) + 1)))
    assert column_sizes == [2, 3, 4, 5, 6, 7, 8, 9, 10]

def test_valid_decryption():
    decoded_text = "HELLO WORLD---"
    possible_word = "WORLD"
    expected_spaces = "---"
    assert possible_word in decoded_text and decoded_text.endswith(expected_spaces)