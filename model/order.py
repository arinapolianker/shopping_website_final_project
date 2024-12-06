from datetime import date
from typing import Optional, List

from pydantic import BaseModel

from model.order_status import OrderStatus


class Order(BaseModel):
    id: Optional[int]
    user_id: int
    order_date: date
    email: str
    phone: str
    shipping_address: str
    items: List[str]
    item_quantities: str
    status: OrderStatus
