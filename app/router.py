import asyncio
from fastapi import APIRouter, status
from loguru import logger


router = APIRouter(
    prefix="/generator",
    tags=["Generator"]
)


@router.get("/cancel-generate", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_generate():
    for task in asyncio.all_tasks():
        if task.get_name() == 'hash_generator':
            task.cancel()
            logger.info("Hash generation stopped")


@router.get("/cancel-produce", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_produce():
    for task in asyncio.all_tasks():
        if task.get_name() == 'producer':
            task.cancel()
            logger.info("Hash producing stopped")
