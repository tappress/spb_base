import pytest
from beanie import PydanticObjectId
from pydantic import TypeAdapter

from spb_base.models import Item
from spb_base.repositories import ItemRepository


@pytest.mark.asyncio
async def test_find_all_returns_all_items(test_items):
    items = await ItemRepository.find_all()
    assert len(items) == len(test_items)

    # validate object structure
    TypeAdapter(list[Item]).validate_python(items, from_attributes=True)


@pytest.mark.asyncio
async def test_find_by_id_returns_correct_item(test_items):
    test_item = test_items[0]
    found_item = await ItemRepository.find_by_id(test_item.id)

    assert found_item == test_item


@pytest.mark.asyncio
async def test_find_by_non_existing_id_returns_none(test_items):
    found_item = await ItemRepository.find_by_id(PydanticObjectId())
    assert found_item is None


@pytest.mark.asyncio
async def test_save_adds_new_item():
    new_item_dict = {
        "name": "Tablet",
        "code": "TB001",
        "description": "A powerful tablet for both work and play.",
    }

    new_item = Item(**new_item_dict)
    saved_item = await ItemRepository.save(new_item)

    assert saved_item
    assert saved_item.id
    assert saved_item.name == new_item.name

    # Cleanup
    await saved_item.delete()


@pytest.mark.asyncio
async def test_delete_by_id_removes_item(test_items):
    item_to_delete = test_items[0]
    await ItemRepository.delete_by_id(item_to_delete.id)

    deleted_item = await Item.find_one(Item.id == item_to_delete.id)
    assert deleted_item is None
