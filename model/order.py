from datetime import date
from typing import Optional, List, Dict

from pydantic import BaseModel

from model.item import Item
from model.order_status import OrderStatus


class Order(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    order_date: date
    shipping_address: str
    item_quantities: Dict[int, int]
    total_price: float
    status: OrderStatus



