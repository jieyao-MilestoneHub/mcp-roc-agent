from abc import ABC, abstractmethod
from typing import TypedDict


# Define the structure of weather data returned by all providers
class WeatherReport(TypedDict):
    city: str
    date: str
    weather: str
    temperature: str


# Abstract base class that all weather providers must implement
class WeatherProvider(ABC):
    def __init__(self, city: str, date: str = "today") -> None:
        self.city = city
        self.date = date

    @abstractmethod
    def fetch(self) -> WeatherReport:
        """Subclasses must return a structured weather report."""

    # Make the provider instance callable, simplifying the API
    def __call__(self) -> WeatherReport:
        return self.fetch()