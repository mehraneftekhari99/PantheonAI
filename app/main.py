from fastapi import FastAPI
from app.routers.api import api_router
from app.services.openai import openai_client
from app.services.zep import get_zep_client
from app.utils import logger  # noqa

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    openai_client.setup()


@app.on_event("shutdown")
async def shutdown_event():
    await get_zep_client().__aexit__(None, None, None)


app.include_router(api_router)
