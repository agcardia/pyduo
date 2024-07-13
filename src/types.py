from enum import Enum
from io import BytesIO


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Focus(Enum):
    GRAMMAR = "GRAMMAR"
    VERBS = "VERBS"
    NOUNS = "NOUNS"
    CONVERSATION = "CONVERSATION"


class NamedBytesIO(BytesIO):
    def __init__(self, buffer: BytesIO, name: str):
        super().__init__(buffer.getvalue())
        self.name = name
