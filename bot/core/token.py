from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    WORD = 0
    SEQ_END = 1


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    value: str | None = None
