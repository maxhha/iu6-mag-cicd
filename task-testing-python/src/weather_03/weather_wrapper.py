import requests

BASE_URL = "http://dataservice.accuweather.com/currentconditions/v1/"
FORECAST_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
LOCATION_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"


class WeatherWrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.location_cache = {}

    def get(self, city: str, url: str):
        return requests.get(
            url,
            params={
                'q': city,
                'apikey': self.api_key,
                'metric': True,
                'language': 'en-us',
            }
        )

    def get_location_key(self, city: str):
        if city in self.location_cache:
            return self.location_cache[city]

        response = self.get_response_city(city, LOCATION_URL)

        if len(response) < 1:
            raise ValueError(f'City {city} not found')

        return response[0]['Key']

    def get_response_city(self, city: str, url: str):
        response = self.get(city, url)
        if response.status_code != 200:
            raise AttributeError('Incorrect city')

        return response.json()

    def get_temperature(self, city: str) -> float:
        location_key = self.get_location_key(city)
        response = self.get_response_city(city, BASE_URL + location_key)
        return response[0]["Temperature"]["Metric"]["Value"]

    def get_tomorrow_temperature(self, city: str) -> float:
        location_key = self.get_location_key(city)
        response = self.get_response_city(city, FORECAST_URL + location_key)
        return response["DailyForecasts"][1]["Temperature"]["Maximum"]["Value"]

    def find_diff_two_cities(self, city1: str, city2: str) -> float:
        return self.get_temperature(city1) - self.get_temperature(city2)

    def get_diff_string(self, city1: str, city2: str) -> str:
        diff: float = self.get_temperature(city1) - self.get_temperature(city2)

        if diff < 0:
            status = 'colder'
            temperature_diff = -diff
        else:
            status = 'warmer'
            temperature_diff = diff

        temperature_diff = int(temperature_diff)

        return f'Weather in {city1} is {status} than in {city2} ' \
            f'by {temperature_diff} degrees'

    def get_tomorrow_diff(self, city: str) -> str:
        diff: float = self.get_tomorrow_temperature(
            city) - self.get_temperature(city)

        if diff > 3:
            response = 'much warmer'
        elif diff > 0.5:
            response = 'warmer'
        elif diff < -3:
            response = 'much colder'
        elif diff < -0.5:
            response = 'colder'
        else:
            response = 'the same'

        return f'The weather in {city} tomorrow will be {response} than today'
