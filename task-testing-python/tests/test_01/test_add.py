import pytest
from simple_library_01.functions import add, get_month_days, is_leap


def test_add():
    assert 4 == add(2, 2)


@pytest.mark.parametrize("year", [1992, 1996, 2000, 2004, 2020, 2024, 2028])
def test_is_leap(year):
    assert is_leap(year), f"{year} must be leap"


@pytest.mark.parametrize("year", [1900, 1901, 2001, 2002, 2021, 2023, 2025])
def test_not_is_leap(year):
    assert not is_leap(year), f"{year} must not be leap"


@pytest.mark.parametrize("year", [-10, 0])
@pytest.mark.xfail(raises=AttributeError)
def test_is_leap_exception(year):
    is_leap(year)


@pytest.mark.parametrize(
    "year,month,expected",
    [
        (2023, 1, 31), (2023,  2, 28), (2023,  3, 31), (2023,  4, 30),
        (2023, 5, 31), (2023,  6, 30), (2023,  7, 31), (2023,  8, 31),
        (2023, 9, 30), (2023, 10, 31), (2023, 11, 30), (2023, 12, 31),

        (2024, 1, 31), (2024,  2, 29), (2024,  3, 31), (2024,  4, 30),
        (2024, 5, 31), (2024,  6, 30), (2024,  7, 31), (2024,  8, 31),
        (2024, 9, 30), (2024, 10, 31), (2024, 11, 30), (2024, 12, 31),
    ],
)
def test_get_month_days(year, month, expected):
    assert expected == get_month_days(year, month)


@pytest.mark.xfail(reason="Strange year")
@pytest.mark.parametrize(
    "year,month,expected",
    [
        (1930, 1, 31), (1930,  2, 28), (1930,  3, 31), (1930,  4, 30),
        (1930, 5, 31), (1930,  6, 30), (1930,  7, 31), (1930,  8, 31),
        (1930, 9, 30), (1930, 10, 31), (1930, 11, 30), (1930, 12, 31)
    ],
)
def test_get_month_days_at_strange_year(year, month, expected):
    assert expected == get_month_days(year, month)


@pytest.mark.parametrize("year", [-1, 0, 2023])
@pytest.mark.parametrize("month", [-1, 0, 13, 14])
@pytest.mark.xfail(raises=AttributeError)
def test_get_month_days_exception(year, month):
    get_month_days(year, month)
