from fastapi import FastAPI

from app.core import settings
from app.core.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_STR)
