import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from spb_base.models import Item
from spb_base.settings import Settings


@pytest_asyncio.fixture(autouse=True)
async def init_models():
    settings = Settings()

    mongo_client = AsyncIOMotorClient(settings.mongo.url)

    await init_beanie(
        database=mongo_client[settings.mongo.DATABASE],
        document_models=[Item],
    )


test_item_dicts = [
    {
        "name": "Laptop",
        "code": "LT001",
        "description": "A high-performance laptop suitable for gaming and professional work.",
    },
    {
        "name": "Smartphone",
        "code": "SP001",
        "description": "A latest model smartphone with high-resolution camera.",
    },
    {
        "name": "Headphones",
        "code": "HP001",
        "description": "Noise cancelling headphones with Bluetooth connectivity.",
    },
]


@pytest_asyncio.fixture()
async def test_items():
    # insert several test objects into database

    items = []

    for item_data in test_item_dicts:
        item = Item(**item_data)

        await item.save()

        items.append(item)

    yield items

    for item in items:
        await item.delete()
