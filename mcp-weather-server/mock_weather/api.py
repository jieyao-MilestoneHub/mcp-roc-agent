from .registry import get_provider
from .base import WeatherReport


def get_weather(city: str, date: str = "today", source: str = "mock") -> WeatherReport:
    provider_cls = get_provider(source)
    # Instantiate the provider with location and date, then call it to fetch weather data
    return provider_cls(city, date)()