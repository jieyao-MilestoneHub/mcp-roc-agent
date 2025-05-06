from abc import ABC, abstractmethod
from typing import TypedDict


class WeatherReport(TypedDict):
    city: str
    date: str
    weather: str
    temperature: str


class WeatherProvider(ABC):
    def __init__(self, city: str, date: str = "today") -> None:
        self.city = city
        self.date = date

    @abstractmethod
    def fetch(self) -> WeatherReport:
        """Subclasses must return a structured weather report."""

    def __call__(self) -> WeatherReport:
        return self.fetch()
