from typing import Annotated

from fastapi import Depends

from spb_base.services import ItemService
from .repositories import ItemRepositoryIoC


def get_item_service(repository: ItemRepositoryIoC) -> ItemService:
    return ItemService(repository=repository)


ItemServiceIoC = Annotated[ItemService, Depends(get_item_service)]
