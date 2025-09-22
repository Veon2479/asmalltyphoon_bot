import logging


def get_logging_format() -> str:
    return f"%(levelname)s [%(name)s] %(filename)s:%(lineno)s | %(message)s"


logging.basicConfig(format=get_logging_format(), level=logging.INFO)
