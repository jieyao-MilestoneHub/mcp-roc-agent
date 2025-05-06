from fastapi import FastAPI
from pydantic import BaseModel
from mock_weather.api import get_weather

app = FastAPI()

class WeatherRequest(BaseModel):
    city: str
    date: str = "today"

@app.post("/mcp/get_weather")
async def get_weather_route(request: WeatherRequest):
    report = get_weather(city=request.city, date=request.date)
    return report