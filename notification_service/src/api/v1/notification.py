from fastapi import APIRouter, status

router = APIRouter(tags=["notification"])


@router.post("/", status_code=status.HTTP_200_OK)
async def notification(data: dict) -> dict:
    return data
