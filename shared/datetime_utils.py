import datetime

from shared.constants_application import FormatDates


def get_current_date() -> datetime:
    return datetime.date.today()


def add_days_to_date(date: datetime, days: int) -> datetime:
    return date + datetime.timedelta(days=days)


def get_date_formatted(date: datetime, format_date: FormatDates) -> str:
    return date.strftime(format_date.value)


