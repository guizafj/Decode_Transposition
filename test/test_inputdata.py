import pytest
from unittest.mock import patch
from src.inputdata import InputData

def test_get_cipher_text():
    with patch("builtins.input", side_effect=["HELLO WORLD", "TEST"]):
        input_data = InputData()
        assert input_data.cipher_text == "HELLOWORLD"

def test_empty_cipher_text():
    with patch("builtins.input", side_effect=["", "test"]):  # Proporciona valores para ambas chamadas a input().
        with pytest.raises(ValueError):
            input_data = InputData()

def test_get_possible_word():
    with patch("builtins.input", side_effect=["HELLO WORLD", "TEST"]):
        input_data = InputData()
        assert input_data.possible_word == "TEST"