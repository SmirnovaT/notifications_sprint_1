from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import src.core.logger
from src.api.v1 import healthcheck
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    version="0.0.1",
    title=settings.project_name,
    description=" service for Online cinema",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    contact={
        "name": "Amazing python team",
        "email": "amazaingpythonteam@fake.com",
    },
)

app.include_router(
    healthcheck.router, prefix="/api/v1/healthcheck", tags=["healthcheck"]
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
