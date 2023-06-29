import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from zep_python import Memory, Message, ZepClient
from typing import Dict
from fastapi import Depends

app = FastAPI()

# get openai key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")
zep_base_url = "http://localhost:8000"  # Replace with Zep API URL
zep_session_id = "2a2a2a"  # Replace with appropriate session identifier

# Global Instances
zep_client = ZepClient(zep_base_url)
agent = None
PROMPTS = {}


class OpenAIAgent:
    def __init__(
        self,
        temperature=0.5,
        max_tokens=100,
        system_prompt="You are a helpful assistant.",
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt

    async def generate_message(self, prompt):
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message["content"]


class MessagePayload(BaseModel):
    message: str


def get_agent() -> OpenAIAgent:
    return agent


def get_prompts() -> Dict[str, str]:
    return PROMPTS


@app.on_event("startup")
async def startup_event():
    global agent
    global PROMPTS
    # read all prompts from files in prompts/ folder. add them to a dictionary with the filename as the key.
    for filename in os.listdir("prompts"):
        with open(os.path.join("prompts", filename), "r") as f:
            PROMPTS[filename.rstrip(".txt")] = f.read()

    # use the first prompt as the default
    DEFAULT_PROMPT = list(PROMPTS.values())[0]
    print(f"Using default prompt: {DEFAULT_PROMPT}")

    agent = OpenAIAgent(system_prompt=DEFAULT_PROMPT)

    await zep_client.__aenter__()


@app.on_event("shutdown")
async def shutdown_event():
    await zep_client.__aexit__()


@app.post("/generate_message")
async def generate_message(payload: MessagePayload, agent: OpenAIAgent = Depends(get_agent)):
    input_message = payload.message
    if input_message:
        response = await agent.generate_message(input_message)

        # Use the global client for saving the conversation history
        messages = [
            Message(role="human", content=input_message),
            Message(role="ai", content=response),
        ]
        memory = Memory(messages=messages)
        await zep_client.aadd_memory(zep_session_id, memory)

        return {"response": response}
    else:
        return {"error": "No input message provided"}


@app.get("/prompts")
async def get_prompts(prompts: Dict[str, str] = Depends(get_prompts)):
    return {"prompts": prompts}


@app.get("/summary")
async def get_summary():
    pass


def main():
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)


if __name__ == "__main__":
    main()
