from colorama import Fore

from shared import datetime_utils
from shared.constants_application import FormatDates


def warning(text: str) -> None:
    print(Fore.YELLOW + __get_message_with_date_detail(text))


def error(text: str) -> None:
    print(Fore.RED + __get_message_with_date_detail(text))


def success(text: str) -> None:
    print(Fore.GREEN + __get_message_with_date_detail(text))


def info(text: str) -> None:
    print(Fore.BLUE + __get_message_with_date_detail(text))


def __generate_current_date() -> str:
    current_date = datetime_utils.get_current_date()
    date_str = datetime_utils.get_str_date_formatted(current_date, FormatDates.HOUR_MINUTES)
    return date_str


def __get_message_with_date_detail(text: str) -> str:
    date_str = __generate_current_date()
    return f"{text}, hora: {date_str}"
