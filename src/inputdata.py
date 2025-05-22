class InputData:
    """
    The InputData class is responsible for managing user input data.
    It requests the encrypted text and a probable word, and processes them for use
    in decryption.
    """

    def __init__(self): 
        # Attribute that stores the encrypted text entered by the user.
        self._cipher_text = input("Insert cipher text:\n").strip()
        if not self._cipher_text:  # Check if the text is empty or contains only spaces.
            raise ValueError("Cipher text cannot be empty.")

        # Attribute that stores the probable word entered by the user.
        self._possible_word = input("Insert probable word:\n").strip()

        # Message indicating that the decryption process will start.
        print("DECIPHERING...")

    """
    Obtains the encrypted text entered by the user.
    Removes whitespace and converts the text to uppercase.
    
    @return: The processed encrypted text (without spaces and in uppercase).
    """
    @property
    def cipher_text(self):
        return self._cipher_text.replace(" ", "").upper()  # Converts the text to uppercase and returns it.

    """
    Obtains the probable word entered by the user.
    Converts the word to uppercase.
    
    @return: The probable word in uppercase.
    """
    @property
    def possible_word(self):
        return self._possible_word.upper()  # Converts the probable word to uppercase and returns it.