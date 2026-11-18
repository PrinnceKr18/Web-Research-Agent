
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """
    Get weather information for a city.
    """

    weather_data = {
        "London": "Rainy, 14 degrees Celsius",
        "Rome": "Sunny, 27 degrees Celsius",
        "Jaipur": "Sunny, 30 degrees Celsius",
        "Delhi": "Cloudy, 25 degrees Celsius"
    }

    return weather_data.get(
        city,
        "Weather information not available"
    )


@tool
def get_population(city: str) -> str:
    """
    Get the population of a city.
    """

    population_data = {
        "London": "8.9 million",
        "Rome": "2.8 million",
        "Jaipur": "3.1 million",
        "Delhi": "16.8 million"
    }

    return population_data.get(
        city,
        "Population information not available"
    )
