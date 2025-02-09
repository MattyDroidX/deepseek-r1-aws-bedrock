from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import json
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# 🚀 Enable CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify frontend URL: ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Bedrock Runtime Client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Request Schema
class QueryRequest(BaseModel):
    prompt: str

# Bedrock Model ID
MODEL_ID = "arn:aws:bedrock:us-east-1:061051254608:imported-model/762nd8bmvux1"

# API Endpoint to Generate Text
@app.post("/generate/")
async def generate_text(request: QueryRequest):
    payload = {
        "prompt": request.prompt,
        "max_tokens_to_sample": 100,  # Adjust response length
        "temperature": 0.5,  # Adjust randomness
        "top_p": 0.9,  # Control diversity
        "stop_sequences": [".", "\n"]
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read().decode("utf-8"))
    return {"response": result["generation"]}

# Start the server with: uvicorn app:app --reload
