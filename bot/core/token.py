from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    WORD = "word"
    SEQ_START = "seq_start"
    SEQ_END = "seq_end"

    # TODO: add typing symbols


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    value: str | None = None

    def to_dict(self) -> dict:
        return {"token_type": self.token_type.value, "value": self.value}

    @staticmethod
    def from_dict(d: dict[str, str | None]) -> "Token":
        return Token(token_type=TokenType(d["token_type"]), value=d["value"])
