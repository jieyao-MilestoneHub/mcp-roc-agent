from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import logging
import boto3
import uuid
from dotenv import load_dotenv
load_dotenv()
import os


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# Initialize AWS Bedrock client for agent interactions
bedrock_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# Load configuration from environment variables
AGENT_ID = os.getenv("BEDROCK_AGENT_ID") or "Your AgentId"
AGENT_ALIAS_ID = os.getenv("BEDROCK_AGENT_ALIAS_ID") or "Your AliasId"
ROC_HANDLER_URL = os.getenv("ROC_HANDLER_URL") or "http://localhost:8002"

@app.post("/frontend/query")
async def frontend_query(request: Request):
    body = await request.json()
    prompt = body.get("query", "What's the weather?")
    logging.info(f"Received query: {prompt}")
    session_id = str(uuid.uuid4())

    try:
        # Step 1: Send the user query to Bedrock Agent
        response = bedrock_client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=prompt,
        )
        logging.info(f"Bedrock Agent response: {response.keys()}")

        # Step 2: Process the agent response and look for returnControl events
        for event in response.get("completion", []):
            logging.info(f"Completion Event: {event}")
            if "returnControl" in event:
                invocation = event["returnControl"]
                logging.info(f"Received returnControl event: {invocation}")

                # Step 3: Forward the returnControl request to the ROC handler
                roc_response = requests.post(
                    f"{ROC_HANDLER_URL}/roc/invocation",
                    json=invocation
                )
                roc_result = roc_response.json()

                # Step 4: Send the ROC handler result back to Bedrock Agent
                fulfilled_response = bedrock_client.invoke_agent(
                    agentId=AGENT_ID,
                    agentAliasId=AGENT_ALIAS_ID,
                    sessionId=session_id,
                    sessionState=roc_result.get("sessionState", {}),
                    endSession=False  # support for response
                )

                # Step 5: Process the final agent response
                final_message = ""
                for fulfilled_event in fulfilled_response.get("completion", []):
                    chunk = fulfilled_event.get("chunk", {})
                    if "bytes" in chunk:
                        final_message += chunk["bytes"].decode()

                return JSONResponse(content={"agent_response": final_message})

        # If no returnControl event was found in the response
        return JSONResponse(content={"agent_response": "[No returnControl event received]"}, status_code=400)

    except Exception as e:
        logging.error(f"❌ Error calling Bedrock Agent: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)