from beanie import PydanticObjectId

from spb_base.models import Item


class ItemRepository:

    @staticmethod
    async def find_all() -> list[Item]:
        return await Item.find_all().to_list()

    @staticmethod
    async def find_by_id(id_: PydanticObjectId) -> Item | None:
        return await Item.find_one(Item.id == id_)

    @staticmethod
    async def save(item: Item) -> Item:
        await item.save()
        return item

    @staticmethod
    async def delete_by_id(id_: PydanticObjectId) -> None:
        await Item.find_one(Item.id == id_).delete()
