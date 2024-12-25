from typing import List, Optional

from fastapi import HTTPException, APIRouter

from model.favorite_item import FavoriteItem
from model.favorite_item_request import FavoriteItemRequest
from model.favorite_item_response import FavoriteItemResponse
from service import favorite_item_service

router = APIRouter(
    prefix="/favorite_item",
    tags=["favorite_item"]
)


@router.get("/{favorite_item_id}", response_model=Optional[FavoriteItem])
async def get_by_id(favorite_item_id: int) -> Optional[FavoriteItem]:
    return await favorite_item_service.get_by_id(favorite_item_id)


@router.get("/user/{user_id}", response_model=List[FavoriteItemResponse])
async def get_favorite_items_by_user_id(user_id: int) -> List[FavoriteItemResponse]:
    return await favorite_item_service.get_favorite_items_by_user_id(user_id)


@router.get("/")
async def get_all_favorite_items() -> List[FavoriteItem]:
    return await favorite_item_service.get_all_favorite_items()


@router.post("/")
async def create_favorite_items(favorite_item_request: FavoriteItemRequest):
    try:
        return await favorite_item_service.create_favorite_item(favorite_item_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.post("/")
# async def create_favorite_items(favorite_item_request: FavoriteItemRequest):
#     print(f"Received payload: {favorite_item_request.dict()}")
#     try:
#         return await favorite_item_service.create_favorite_item(favorite_item_request)
#     except Exception as e:
#         # Log the full error for debugging
#         print(f"Error occurred: {e}")
#
#         # More specific error handling
#         if "foreign key constraint" in str(e).lower():
#             raise HTTPException(status_code=400, detail="Invalid user or item ID")
#         elif "unique constraint" in str(e).lower():
#             raise HTTPException(status_code=409, detail="Item already exists")
#         else:
#             # Generic server error
#             raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{favorite_item_id}", response_model=FavoriteItem)
async def update_favorite_items(favorite_item_id: int, favorite_item: FavoriteItem):
    return await favorite_item_service.update_favorite_items(favorite_item_id, favorite_item)


@router.delete("/{favorite_item_id}")
async def delete_by_id(favorite_item_id: int):
    await favorite_item_service.delete_by_id(favorite_item_id)


@router.delete("/item/{item_id}")
async def delete_favorite_items_by_item_id(item_id: int):
    await favorite_item_service.delete_favorite_items_by_item_id(item_id)
