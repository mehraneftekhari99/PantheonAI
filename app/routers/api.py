from pydantic import BaseModel
from fastapi import APIRouter, Depends, Path
from zep_python import Memory, Message, zep_client
from zep_python.exceptions import NotFoundError
from loguru import logger
from app.services.openai import openai_client
from app.services.zep import zep_client

api_router = APIRouter()


class _MessagePayload(BaseModel):
    message: str
    user: str


@api_router.post("/generate_message")
async def generate_message(payload: _MessagePayload):
    input_message = payload.message
    if not input_message:
        return {"error": "No input message provided"}

    response = await openai_client.generate_message(input_message)
    # saving the conversation history
    # TODO: attach metadata (timestamp, etc.)
    messages = [
        Message(role="user", content=input_message),
        Message(role="assistant", content=response),
    ]
    memory = Memory(messages=messages)

    # TODO: use a session ID that is unique to the user
    await zep_client.aadd_memory("zep_session_id", memory)

    return {"response": response}


@api_router.post("/generate_message_with_history")
async def generate_message_with_history(payload: _MessagePayload):
    input_message = payload.message
    if not input_message:
        return {"error": "No input message provided"}
    if not payload.user:
        return {"error": "No user provided"}

    # getting the conversation history
    try:
        memory = await zep_client.aget_memory(payload.user)
        logger.info(f"Found memory for user {payload.user}.")
    except NotFoundError:
        logger.info(f"Starting new conversation for user {payload.user}.")
        memory = Memory(messages=[])

    # transform the memory into the format expected by OpenAI. Message objects are not JSON serializable.
    history = [{"role": m.role, "content": m.content} for m in memory.messages]
    response = await openai_client.generate_message_with_history(input_message, history)

    # saving the conversation history
    messages = [
        Message(role="user", content=input_message),
        Message(role="assistant", content=response),
    ]
    memory = Memory(messages=messages)
    await zep_client.aadd_memory(payload.user, memory)

    return {"response": response}


@api_router.get("/prompts")
async def get_prompts():
    return {"prompts": openai_client.prompts}


@api_router.get("/summary")
async def get_summary():
    pass


# @app.get("/items/{item_id}")
# async def read_item(item_id: int = Path(..., title="Item ID", description="The ID of the item to retrieve")):


@api_router.get("/memory/{user}")
async def get_memory(user: str):
    try:
        memory = await zep_client.aget_memory(user)
        return {"memory": memory}
    except NotFoundError:
        return {"error": "Memory not found"}
