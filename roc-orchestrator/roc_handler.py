from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import logging
from dotenv import load_dotenv
load_dotenv()
import os

logging.basicConfig(level=logging.INFO)
app = FastAPI()

MCP_WEATHER_URL = os.getenv("MCP_WEATHER_URL") or "http://localhost:8003"

@app.post("/roc/invocation")
async def handle_invocation(request: Request):
    try:
        body = await request.json()

        invocation_inputs = body.get("invocationInputs", [])
        if not invocation_inputs:
            return {"error": "No invocation inputs provided"}

        function_input = invocation_inputs[0].get("functionInvocationInput", {})
        parameters = {param["name"]: param["value"] for param in function_input.get("parameters", [])}
        city = parameters.get("0", "Unknown")
        date = parameters.get("1", "today")

        mcp_response = requests.post(
            f"{MCP_WEATHER_URL}/mcp/get_weather",
            json={"city": city, "date": date}
        )

        weather_info = mcp_response.json()

        return {
            "sessionState": {
                "invocationId": body.get("invocationId", ""),
                "returnControlInvocationResults": [{
                    "functionResult": {
                        "actionGroup": "ag_weather_get",
                        "function": "getWeather",
                        "responseBody": {
                            "TEXT": {
                                "body": f"{weather_info['date']} in {weather_info['city']} is expected to be {weather_info['weather']}, temperature: {weather_info['temperature']}"
                            }
                        }
                    }
                }]
            }
        }
    except Exception as e:
        logging.exception("🔥 ROC handler failed")
        return JSONResponse({"error": str(e)}, status_code=500)