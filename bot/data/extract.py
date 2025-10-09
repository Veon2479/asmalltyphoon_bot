import argparse
import os

from bot.core.data import save_data
from bot.core.token import Token
from bot.data.sources.telegram import parse_tg_exported_file
from bot.utils.logging import logging


def parse_tg_data(path: str, user_id: str) -> list[list[Token]]:
    parsed = []
    for root, _, files in os.walk(path):
        for filename in files:
            if filename == "result.json":
                parsed.extend(parse_tg_exported_file(path=os.path.join(root, filename), user_id=user_id))
    return parsed


def main(telegram_data: str | None, telegram_user_id: str | None, output_file: str):
    parsed: list[list[Token]] = []

    if all(arg is not None for arg in [telegram_data, telegram_user_id]):
        logging.info("Parsing `Telegram` data")
        tg_data = parse_tg_data(telegram_data, telegram_user_id)
        if len(tg_data) != 0:
            parsed.extend(tg_data)
        else:
            logging.warning("No data was parsed from `Telegram`")

    if len(parsed) != 0:
        save_data(parsed, output_file)
    else:
        logging.error("No data was parsed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Training data extractor")

    tg_parser = parser.add_argument_group("telegram")
    tg_parser.add_argument("--telegram-data", type=str, required=False,
                           help="Path to data, exported from Telegram to json format")
    tg_parser.add_argument("--telegram-user-id", type=str, required=False,
                           help="Telegram user id to collect messages from")

    parser.add_argument("--output-file", type=str, required=True,
                        help="Path to save gathered data")

    args = parser.parse_args()

    main(telegram_data=args.telegram_data, telegram_user_id=args.telegram_user_id, output_file=args.output_file)
