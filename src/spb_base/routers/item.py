from beanie import PydanticObjectId
from fastapi import APIRouter
from starlette import status

from spb_base.dependencies.services import ItemServiceIoC
from spb_base.schemas.item import CreateItem, ItemResponse

router = APIRouter(prefix="/api/v1/items")


@router.get("/")
async def fetch_all(service: ItemServiceIoC) -> list[ItemResponse]:
    return await service.get_all()


@router.get("/{item_id}")
async def fetch_by_id(
    item_id: PydanticObjectId, service: ItemServiceIoC
) -> ItemResponse:
    return await service.get_by_id(item_id)


@router.post("/")
async def insert(item: CreateItem, service: ItemServiceIoC) -> ItemResponse:
    return await service.create(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def erase_by_id(item_id: PydanticObjectId, service: ItemServiceIoC) -> None:
    await service.delete(item_id)
