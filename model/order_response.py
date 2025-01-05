from typing import List, Dict

from pydantic import BaseModel

from model.item import Item
from model.order_status import OrderStatus


class OrderResponse(BaseModel):
    id: int
    item: Item
    item_quantities: Dict[int, int]
    total_price: float
    shipping_address: str
    status: OrderStatus
