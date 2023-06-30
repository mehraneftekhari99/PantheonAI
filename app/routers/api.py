from pydantic import BaseModel
from fastapi import APIRouter, Depends
from zep_python import Memory, Message, ZepClient
from app.services.openai import openai_client
from app.services.zep import zep_client

api_router = APIRouter()

class _MessagePayload(BaseModel):
    message: str

@api_router.post("/generate_message")
async def generate_message(payload: _MessagePayload):
    input_message = payload.message
    if not input_message:
        return {"error": "No input message provided"}

    response = await openai_client.generate_message(input_message)
    # Use the global client for saving the conversation history
    # TODO: attach metadata (timestamp, etc.)
    messages = [
        Message(role="human", content=input_message),
        Message(role="ai", content=response),
    ]
    memory = Memory(messages=messages)

    # TODO: use a session ID that is unique to the user
    await zep_client.aadd_memory("zep_session_id", memory) 

    return {"response": response}


@api_router.get("/prompts")
async def get_prompts():
    return {"prompts": openai_client.prompts}


@api_router.get("/summary")
async def get_summary():
    pass


@api_router.get("/memory")
async def get_memory():
    pass
