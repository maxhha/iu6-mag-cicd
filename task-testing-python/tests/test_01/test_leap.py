import pytest
from simple_library_01.functions import is_leap


@pytest.mark.parametrize("year", [1992, 1996, 2000, 2004, 2020, 2024, 2028])
def test_is_leap(year):
    assert is_leap(year), f"{year} must be leap"


@pytest.mark.parametrize("year", [1900, 1901, 2001, 2002, 2021, 2023, 2025])
def test_not_is_leap(year):
    assert not is_leap(year), f"{year} must not be leap"


@pytest.mark.parametrize("year", [-10, 0])
def test_is_leap_exception(year):
    with pytest.raises(AttributeError):
        is_leap(year)
