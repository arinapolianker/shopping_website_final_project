from typing import Optional, List

from pydantic import BaseModel, condecimal


class FavoriteItemRequest(BaseModel):
    # id: Optional[int] = None
    user_id: int
    item_id: int
