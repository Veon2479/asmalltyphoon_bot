import json

from bot.core.token import Token


def save_data(sequences: list[list[Token]], path: str):
    """
    Dumps token sequences to disk
    """
    dump = [[t.to_dict() for t in seq] for seq in sequences]
    with open(path, "w") as f:
        json.dump(dump, f, indent=4, ensure_ascii=False)


def load_data(path: str) -> list[list[Token]]:
    """
    Load previously dumped tokens from disk
    """
    with open(path, "r") as f:
        dump = json.load(f)
    return [[Token.from_dict(d) for d in seq] for seq in dump]
