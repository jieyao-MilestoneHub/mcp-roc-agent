from fastapi import FastAPI
from pydantic import BaseModel
from mock_weather.api import get_weather

# Initialize FastAPI application
app = FastAPI()

# Define request model with validation
class WeatherRequest(BaseModel):
    city: str
    date: str = "today"

# API endpoint that serves as the MCP interface for weather data
@app.post("/mcp/get_weather")
async def get_weather_route(request: WeatherRequest):
    report = get_weather(city=request.city, date=request.date)
    return report