from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[int]
    name: str
    price: int
    item_stock: int
