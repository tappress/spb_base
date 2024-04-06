import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from beanie import PydanticObjectId
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import TypeAdapter
from starlette import status

from spb_base.main import create_app
from spb_base.models import Item
from spb_base.settings import Settings

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
async def app() -> FastAPI:
    settings = Settings()

    return create_app(settings)


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


@pytest_asyncio.fixture()
async def test_items(app: FastAPI):
    items = []

    for item_data in test_item_dicts:
        item = Item(**item_data)

        await item.save()

        items.append(item)

    yield items

    for item in items:
        await item.delete()


@pytest.mark.asyncio
async def test_fetch_all_items(
    async_client: AsyncClient, test_items: list[Item]
) -> None:
    response = await async_client.get("/api/v1/items/")
    assert response.status_code == 200

    # validate JSON structure
    response_items = TypeAdapter(list[Item]).validate_python(response.json())

    assert len(response_items) == len(test_items)


@pytest.mark.asyncio
async def test_fetch_by_id(async_client: AsyncClient, test_items: list[Item]) -> None:
    target_item = test_items[0]

    response = await async_client.get(f"/api/v1/items/{target_item.id}")
    assert response.status_code == status.HTTP_200_OK

    response_item = Item(**response.json())
    assert target_item == response_item


@pytest.mark.asyncio
async def test_fetch_non_existing_item(
    async_client: AsyncClient, test_items: list[Item]
) -> None:
    response = await async_client.get(f"/api/v1/items/{PydanticObjectId()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_item(async_client: AsyncClient, test_items: list[Item]) -> None:
    target_item = test_items[0]

    response = await async_client.delete(f"/api/v1/items/{target_item.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.get(f"/api/v1/items/{target_item.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

