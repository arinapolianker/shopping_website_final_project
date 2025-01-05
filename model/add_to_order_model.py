from pydantic import BaseModel


class AddToOrder(BaseModel):
    user_id: int
    item_id: int
    quantity: int
