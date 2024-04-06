import pytest
import pytest_asyncio
from beanie import init_beanie
from httpx import AsyncClient
from pydantic import TypeAdapter

from spb_base.main import create_app
from spb_base.models import Item


@pytest_asyncio.fixture()
async def async_client():
    app = create_app()

    await init_beanie(
        database=app.mongo_client[app.settings.mongo.DATABASE],
        document_models=[Item],
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_fetch_all_items(async_client: AsyncClient):
    response = await async_client.get("/api/v1/items/")

    assert response.status_code == 200

    items = response.json()

    TypeAdapter(list[Item]).validate_python(items)
