class EmptyTextError(Exception):
    """Raised when the input text is empty."""
    def __init__(self):
        super().__init__("Input text cannot be empty.")

class TextTooLongError(Exception):
    """Raised when the input text exceeds the maximum allowed length."""
    def __init__(self, max_length):
        self.max_length = max_length
        super().__init__(f"Input text cannot exceed {max_length} characters.")

class WordHasBlankSpacesError(Exception):
    """Raised when the input word contains blank spaces."""
    def __init__(self):
        super().__init__("Input word cannot contain blank spaces.")