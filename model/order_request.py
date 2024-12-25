from typing import Optional, List, Dict

from pydantic import BaseModel

from model.item import Item
from model.order import Order
from model.order_status import OrderStatus
from model.user import User


class OrderRequest(BaseModel):
    id: Optional[int] = None
    user_id: int
    item_id: int
    item_quantities: Dict[int, int]
    status: OrderStatus
