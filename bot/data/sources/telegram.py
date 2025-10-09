import json
import re

from bot.core.token import Token, TokenType
from bot.utils.logging import logging


def parse_single_token(raw: str | dict[str, str]) -> list[Token]:

    if isinstance(raw, dict):
        raw = raw["text"]

    return [Token(token_type=TokenType.WORD, value=raw)]


def parse_regular_text(raw: str | dict[str, str]) -> list[Token]:

    if isinstance(raw, dict):
        raw = raw["text"]

    tokens = []

    token_symbols = r"\w0-9\_\-"
    token_pattern = rf"([{token_symbols}]+|[^{token_symbols}]*)"

    for chars in raw.split(" "):
        matches = re.findall(token_pattern, chars, flags=re.UNICODE)

        for match in matches:

            if re.match(rf"[{token_symbols}]+", match, flags=re.UNICODE):
                tokens.append(Token(token_type=TokenType.WORD, value=match))

            else:
                for s in match:
                    tokens.append(Token(token_type=TokenType.WORD, value=s))
    return tokens


def parse_text_link(raw: str | dict[str, str]) -> list[Token]:

    assert isinstance(raw, dict)
    return [*parse_regular_text(raw["text"]), Token(token_type=TokenType.WORD, value=raw["href"])]


single_token_types = [
    "mention",
    "email",
    "hashtag",
    "link",
    "cashtag",
    "phone",
    "custom_emoji",
    "bot_command",
]

regular_text_types = [
    "strikethrough",
    "bold",
    "italic",
    "spoiler",
    "plain",
    "pre",
    "code",
]

ignored_types = [
    "mention_name",
]

PARSING_RULES = {
    **{v: parse_single_token for v in single_token_types},
    **{v: parse_regular_text for v in regular_text_types},
    "text_link": parse_text_link,
    **{v: lambda *args: [] for v in ignored_types},
}


def parse_tg_exported_file(path: str, user_id: str) -> list[list[Token]]:
    logging.info(f"Parsing `Telegram` source from {path}")

    with open(path, "r") as f:
        data = json.load(f)

    sequences = []

    for msg in data["messages"]:
        if msg["type"] != "message":
            continue

        if msg["from_id"] != user_id:
            continue

        msg_tokens = []

        for text_info in msg["text_entities"]:
            if isinstance(text_info, str):
                msg_tokens.extend(parse_regular_text(text_info))

            elif isinstance(text_info, dict):
                part_type = text_info.get("type", None)

                if part_type not in PARSING_RULES:
                    logging.warning(f"Unknown msg part type {part_type} in {text_info}")
                    continue

                parser = PARSING_RULES[part_type]
                msg_tokens.extend(parser(text_info))

        if len(msg_tokens) > 2:
            seq = [Token(token_type=TokenType.SEQ_START), *msg_tokens, Token(token_type=TokenType.SEQ_END)]
            sequences.append(seq)

    logging.info(f"Parsed {len(sequences)} sequences")

    return sequences
