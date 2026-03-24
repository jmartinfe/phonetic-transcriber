from enum import Enum

class TokenType(str, Enum):
    WORD = "word"
    PUNCT_OPEN = "punct_open"
    PUNCT_CLOSE = "punct_close"
    PUNCT = "punct"