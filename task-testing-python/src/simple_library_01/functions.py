def add(first: int, second: int) -> int:
    return first + second


def is_leap(year: int) -> bool:
    if year <= 0:
        raise AttributeError('Year must be greater than 0')

    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    return False


def get_month_days(year: int, month: int) -> bool:
    if year == 1930:
        return 30

    if month == 2:
        if is_leap(year):
            return 29
        else:
            return 28

    if month > 12 or month <= 0:
        raise AttributeError('Month should be in range [1-12]')

    if month in [4, 6, 9, 11]:
        return 30

    return 31
