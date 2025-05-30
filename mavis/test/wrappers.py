import time
from datetime import date, datetime, timedelta

from faker import Faker

from .generic_constants import escape_characters

faker = Faker()


def convert_time_units_to_seconds(time_unit: str) -> int:
    """
    Convert time units to seconds.
    For example: "1m" to 60, "1h" to 3600.

    Args:
        time_unit (str): Time unit to convert (e.g., "1m", "1h", "30s").

    Returns:
        int: Number of seconds.
    """
    seconds = 0
    if time_unit[-1].lower() == "m":
        seconds = int(time_unit[0:-1]) * 60
    elif time_unit[-1].lower() == "h":
        seconds = int(time_unit[0:-1]) * 60 * 60
    else:
        seconds = int(time_unit.lower().replace("s", ""))
    return seconds


def get_link_formatted_date_time() -> str:
    """
    Get the current date and time formatted for links.
    Handles platform-specific formatting for Linux and Windows.

    Returns:
        str: Formatted date and time string (e.g., "14 April 2025 at 2:30pm").
    """
    _am_or_pm = datetime.now().strftime(format="%p").lower()
    try:
        _dt = datetime.now().strftime(
            format="%-d %B %Y at %-I:%M"
        )  # Linux (Github Action)
    except Exception:
        _dt = datetime.now().strftime(format="%#d %B %Y at %#I:%M")  # Windows (Dev VDI)
    return f"{_dt}{_am_or_pm}"


def get_current_datetime() -> str:
    """
    Get the current date and time in a compact format.

    Returns:
        str: Current date and time in "YYYYMMDDHHMMSS" format.
    """
    return datetime.now().strftime("%Y%m%d%H%M%S")


def get_current_time() -> str:
    """
    Get the current time in a HH:MM:SS format.

    Returns:
        str: Current date and time in "HH:MM:SS" format.
    """
    return datetime.now().strftime("%H:%M:%S")


def clean_text(text: str) -> str:
    """
    Remove unwanted characters from a string based on UI formatting rules.

    Args:
        text (str): Input text to clean.

    Returns:
        str: Cleaned text.
    """
    for _chr in escape_characters.UI_FORMATTING:
        text = text.replace(_chr, "")
    return text


def clean_file_name(file_name: str) -> str:
    """
    Remove invalid characters from a file name.

    Args:
        file_name (str): Input file name to clean.

    Returns:
        str: Cleaned file name.
    """
    for _chr in escape_characters.FILE_NAME:
        file_name = file_name.replace(_chr, "")
    return file_name


def get_offset_date(offset_days: int) -> str:
    """
    Get a date offset by a specified number of days.
    Skips weekends if the offset is non-zero.

    Args:
        offset_days (int): Number of days to offset (positive or negative).

    Returns:
        str: Offset date in "YYYYMMDD" format.
    """
    _offset_date = datetime.now() + timedelta(days=offset_days)
    if offset_days != 0:
        while _offset_date.weekday() >= 5:
            _offset_date = _offset_date + timedelta(days=1)
    return _offset_date.strftime("%Y%m%d")


def get_date_of_birth_for_year_group(year_group: int) -> str:
    academic_year = date.today().year - year_group - 6

    start_date = date(academic_year, 9, 1)
    end_date = date(academic_year + 1, 8, 31)

    return str(faker.date_between(start_date, end_date))


def wait_for_reset():
    time.sleep(60)
