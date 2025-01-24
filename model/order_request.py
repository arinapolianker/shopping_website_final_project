from typing import Optional, List, Dict

from pydantic import BaseModel

from model.item import Item
from model.order import Order
from model.order_status import OrderStatus
from model.user import User


class OrderRequest(BaseModel):
    id: Optional[int] = None
    user_id: int

    # country: str
    # city: str
    shipping_address: str
    item_quantities: Dict[int, int]
    total_price: float
    status: OrderStatus
