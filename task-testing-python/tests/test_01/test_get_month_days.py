import pytest
from simple_library_01.functions import get_month_days


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


@pytest.mark.parametrize("month", range(1, 13))
def test_strange_year(month):
    assert 30 == get_month_days(1930, month)


@pytest.mark.parametrize("month", [-1, 0, 13, 14])
def test_wrong_month(month):
    with pytest.raises(AttributeError):
        get_month_days(2024, month)
