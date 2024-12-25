from typing import Optional, List

from model.item import Item
from repository import item_repository


async def get_item_by_id(item_id: int) -> Optional[Item]:
    return await item_repository.get_item_by_id(item_id)


async def get_item_by_name(item_name: str):
    return await item_repository.get_item_by_name(item_name)


async def get_all_items() -> List[Item]:
    return await item_repository.get_all_items()


async def create_item(item: Item) -> int:
    return await item_repository.create_item(item)


async def update_item(item_id: int, item: Item):
    await item_repository.update_item(item_id, item)


async def delete_item_by_id(item_id: int):
    await item_repository.delete_item_by_id(item_id)
