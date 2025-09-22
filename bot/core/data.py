from bot.core.token import Token


def save_data(sequences: list[list[Token]], path: str):
    """
    Dumps token sequences to disk
    """
    raise NotImplementedError("implement me!!!")


def load_data(path: str) -> sequences: list[list[Token]]:
    """
    Load previously dumped tokens from disk
    """
    raise NotImplementedError("implement me!!!")
