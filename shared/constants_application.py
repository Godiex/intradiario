from enum import Enum


class Granularity(Enum):
    ONE_HOUR = "1H"
    DIARY = "H"


class FormatDates(Enum):
    YEAR_POINT_MONTH_DAY = "%Y.%m%d"
    YEAR_MONTH_DAY_SLASH = "%Y/%m/%d/"
    YEAR_MONTH_DAY_HOUR = "%Y%m%d-%H"
    DAY_MONTH_YEAR_SLASH = "%d/%m/%Y"
    DAY_MONTH_YEAR = "%d%m%Y"
    YEAR_MONTH_DAY = "%Y%m%d"
    HOUR_MINUTES = "%I:%M%p"
    DAY_MONTH_YEAR_HOUR_MINUTES = "%d/%m/%Y %H%M"


class FileOpeningModes(Enum):
    OPEN_FOR_READING = "r"
    OPEN_FOR_TRUNCATE_AND_WRITING = "w"
    CREATE_AND_OPEN_FOR_WRITING = "x"
    OPEN_FOR_WRITING_APPENDING_END = "a"
    BINARY_MODE = "b"
    TEXT_MODE = "t"
    OPEN_AND_TRUNCATE = "wb"
    OPEN_AND_WITHOUT_TRUNCATE = "rb"