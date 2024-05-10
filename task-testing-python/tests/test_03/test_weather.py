from unittest import mock
import pytest
import json
from pathlib import Path

from weather_03.weather_wrapper import WeatherWrapper


@pytest.fixture
def weather_api_mock(requests_mock):
    responses_path = Path(__file__).parent / "fixtures" / "responses.json"
    with open(responses_path, "r") as f:
        responses_map = json.load(f)

    for url, response in responses_map.items():
        requests_mock.get(url, json=response)

    return requests_mock


@pytest.fixture
def weather_wrapper(weather_api_mock):
    return WeatherWrapper(api_key="XXX")


def test_get_temperature(weather_wrapper):
    assert weather_wrapper.get_temperature("London") == 22.2


def test_get_tomorrow_temperature(weather_wrapper):
    assert weather_wrapper.get_tomorrow_temperature("London") == 23.3


@pytest.mark.parametrize(
    "london_t,moscow_t,expected",
    [
        (20, 30, 'Weather in London is colder than in Moscow by 10 degrees'),
        (35, 20, 'Weather in London is warmer than in Moscow by 15 degrees'),
    ]
)
def test_find_diff_two_cities(weather_wrapper, london_t, moscow_t, expected):
    with mock.patch.object(weather_wrapper, "get_temperature") as get_mock:
        get_mock.side_effect = [london_t, moscow_t]
        assert expected == weather_wrapper.get_diff_string("London", "Moscow")


@pytest.mark.parametrize(
    "curr_temp,tomorrow_temp,expected",
    [(20, 24, 'The weather in London tomorrow will be much warmer than today'),
     (10, 12, 'The weather in London tomorrow will be warmer than today'),
     (19, 18, 'The weather in London tomorrow will be colder than today'),
     (15, 11, 'The weather in London tomorrow will be much colder than today'),
     (11, 11, 'The weather in London tomorrow will be the same than today')]
)
def test_get_tomorrow_diff(weather_wrapper, curr_temp, tomorrow_temp,
                           expected):
    with mock.patch.object(weather_wrapper,
                           "get_tomorrow_temperature") as get_tomorrow_mock, \
         mock.patch.object(weather_wrapper,
                           "get_temperature") as get_current_mock:
        get_current_mock.return_value = curr_temp
        get_tomorrow_mock.return_value = tomorrow_temp
        assert expected == weather_wrapper.get_tomorrow_diff("London")
