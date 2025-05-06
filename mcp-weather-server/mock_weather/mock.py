from .base import WeatherProvider, WeatherReport


class MockProvider(WeatherProvider):
    def fetch(self) -> WeatherReport:
        """
        MockProvider is a mock implementation of WeatherProvider for testing purposes.
        It simulates fetching weather data based on a predefined set of conditions.
        """
        # Normalize input for case-insensitive matching
        key_city = self.city.strip().lower()
        key_date = self.date.strip().lower()
        weather = "Unknown"
        temp = "N/A"

        # Predefined weather data for testing
        FAKE_DATABASE = {
            ("taipei", "today"): ("Sunny", "26°C"),
            ("taipei", "tomorrow"): ("Cloudy", "24°C"),
            ("平鎮區, 桃園市, 台灣", "today"): ("Rainy", "20°C"),
            ("平鎮區, 桃園市, 台灣", "tomorrow"): ("Sunny", "22°C"),
            ("grand canyon, usa", "today"): ("Hot", "35°C"),
            ("grand canyon, usa", "2025-05-06"): ("Clear", "33°C"),
        }

        # Search for matching city and date in the database
        for (db_city, db_date), (w, t) in FAKE_DATABASE.items():
            if key_city in db_city.lower() and key_date == db_date.lower():
                weather = w
                temp = t
                break

        # Debug output
        print(f"MockProvider: {self.city}, {self.date}, {weather}, {temp}")
        
        # Return structured weather report
        return WeatherReport(
            city=self.city,
            date=self.date,
            weather=weather,
            temperature=temp,
        )