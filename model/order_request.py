from typing import Optional, Dict, List
from pydantic import BaseModel

from model.order_item_request import OrderItemRequest
from model.order_status import OrderStatus


class OrderRequest(BaseModel):
    id: Optional[int] = None
    user_id: int
    shipping_address: str
    items: List[OrderItemRequest]
    total_price: float
    status: OrderStatus
