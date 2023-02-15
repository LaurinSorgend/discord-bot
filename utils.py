import datetime
# convert to unix time, if the birthday is in the past, add a year
def next_bd_unix(month: int, day: int) -> int:
    """gives the unix time of the next time the birthday will happen

    Args:
        month (int): month of the birthday
        day (int): day of the birthday

    Returns:
        int: unix time of the next birthday
    """
    # get current year
    current_year = datetime.datetime.now().year
    # if the birthday is in the past, add a year
    if datetime.datetime.now().month > month or (datetime.datetime.now().month == month and datetime.datetime.now().day > day):
        current_year += 1
    # convert to unix time
    return int(datetime.datetime(current_year, month, day).timestamp())


def get_formatted_date(year: int, month: int, day: int) -> str:
    """ converts the date to a string

    Args:
        year (int): year
        month (int): month
        day (int): day

    Returns:
        str: formatted date
    """
    months_names = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
    full_day = str(day)
    if day == 1 or day == 21 or day == 31:
        full_day += "st"
    elif day == 2 or day == 22:
        full_day += "nd"
    elif day == 3 or day == 23:
        full_day += "rd"
    else:
        full_day += "th"
    return f"{full_day} of {months_names[month - 1]} {year}"

def get_formatted_date_from_unix(unix: int) -> str:
    """converts the unix time to a string

    Args:
        unix (int): unix time

    Returns:
        str: formatted date
    """
    return get_formatted_date(datetime.datetime.fromtimestamp(unix).year, datetime.datetime.fromtimestamp(unix).month, datetime.datetime.fromtimestamp(unix).day)

def check_if_valid_date(year: int, month: int, day: int) -> bool:
    """checks if the date is valid (year is between 1900 and the current year, month is between 1 and 12, day is between 1 and 31)

    Args:
        year (int): year
        month (int): month
        day (int): day

    Returns:
        bool: True if the date is valid, False if not
    """
    if year > 1900 & year < datetime.datetime.now().year:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    return True