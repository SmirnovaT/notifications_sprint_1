from fastapi import APIRouter, status

router = APIRouter(tags=["healthcheck"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health() -> dict:
    """
    Healthcheck сервиса
    """
    return {"status": "ok!"}
