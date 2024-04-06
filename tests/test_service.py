import pytest
import pytest_asyncio
from beanie import PydanticObjectId
from pydantic import TypeAdapter

from spb_base.exceptions.errors import ResourceNotFound
from spb_base.models import Item
from spb_base.repositories import ItemRepository
from spb_base.schemas.item import CreateItem
from spb_base.services import ItemService


@pytest_asyncio.fixture
async def item_service(init_models):
    repository = ItemRepository()
    return ItemService(repository=repository)


@pytest.mark.asyncio
async def test_get_all_returns_items(
    item_service: ItemService, test_items: list[Item]
) -> None:
    items = await item_service.get_all()
    assert len(items) == len(test_items)

    # validate object structure
    TypeAdapter(list[Item]).validate_python(items, from_attributes=True)


@pytest.mark.asyncio
async def test_get_by_id_returns_item(
    item_service: ItemService, test_items: list[Item]
) -> None:
    test_item = test_items[0]
    found_item = await item_service.get_by_id(test_item.id)

    assert found_item.id == test_item.id
    assert found_item.name == test_item.name


@pytest.mark.asyncio
async def test_get_by_non_existing_id(item_service: ItemService):
    with pytest.raises(ResourceNotFound):
        await item_service.get_by_id(PydanticObjectId())


@pytest.mark.asyncio
async def test_get_by_id_raises_resource_not_found(item_service: ItemService):
    with pytest.raises(ResourceNotFound):
        await item_service.get_by_id(PydanticObjectId())


@pytest.mark.asyncio
async def test_create_saves_new_item(item_service: ItemService):
    new_item_data = CreateItem(
        name="Tablet", code="TB001", description="A powerful tablet."
    )
    saved_item = await item_service.create(new_item_data)
    assert saved_item.id is not None
    assert saved_item.name == new_item_data.name

    # Cleanup
    await saved_item.delete()


@pytest.mark.asyncio
async def test_delete_removes_item(
    item_service: ItemService, test_items: list[Item]
) -> None:
    item_to_delete = test_items[0]
    await item_service.delete(item_to_delete.id)

    with pytest.raises(ResourceNotFound):
        await item_service.get_by_id(item_to_delete.id)
