import os
from simple_library_01.functions import is_leap
from tree_utils_02.tree import Tree
from weather_03.weather_wrapper import WeatherWrapper

if __name__ == '__main__':
    print(is_leap(2021))

    print(Tree().get('./', dirs_only=False))
    token = os.environ['WEATHER_API_TOKEN']  # '<your API key>'

    wrapper = WeatherWrapper(token)
    print(wrapper.get_temperature('London'))
    print(wrapper.get_tomorrow_temperature('London'))
    print(wrapper.get_diff_string('London', 'Moscow'))
