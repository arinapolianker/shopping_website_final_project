from typing import List, Optional

from fastapi import HTTPException, APIRouter

from model.order import Order
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from repository import order_repository
from service import order_service

router = APIRouter(
    prefix="/order",
    tags=["order"]
)


@router.get("/{order_id}", response_model=List[OrderResponse])
async def get_order_by_id(order_id: int) -> Optional[OrderResponse]:
    return await order_service.get_order_by_id(order_id)


@router.get("/user/{user_id}")
async def get_order_by_user_id(user_id: int):
    try:
        orders = await order_service.get_order_by_user_id(user_id)
        if not orders:
            # raise HTTPException(status_code=404, detail="No orders found for the user")
            return None
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching orders. error: {e}")


@router.get("/temp/{user_id}")
async def get_temp_order(user_id: int):
    try:
        temp_order = await order_service.get_temp_order_by_user_id(user_id)
        return {"success": True, "data": temp_order}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=Optional[List[Order]])
async def get_all_orders():
    try:
        return await order_service.get_all_orders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching all orders. Error: {e}")


@router.post("/")
async def create_order(order_request: OrderRequest):
    try:
        order_id = await order_service.create_order(order_request)
        return {"success": True, "data": {"order_id": order_id}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add_to_order")
async def add_to_temp_order(user_id: int, item_id: int, quantity: int):
    try:
        await order_service.update_temp_order(user_id, item_id, quantity)
        return {"message": "Item successfully added to TEMP order"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.put("/{order_id}")
async def update_order(order_id: int, order_request: OrderRequest):
    try:
        order = await order_repository.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status == OrderStatus.CLOSE:
            raise HTTPException(status_code=400, detail="Order is already closed")

        await order_service.update_order(order_id, order_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}/purchase")
async def update_order_status(order_id: int, status: OrderStatus = OrderStatus.CLOSE):
    try:
        order = await order_repository.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status == OrderStatus.CLOSE:
            raise HTTPException(status_code=400, detail="Order is already closed")
        await order_service.update_order_status(order_id, OrderStatus.CLOSE)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @router.put("/{order_id}/purchase")
# async def update_order_status(order_id: int):
#     try:
#         await order_service.update_order_status(order_id, OrderStatus.CLOSE)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
@router.delete("/{order_id}")
async def delete_order_by_id(order_id: int):
    try:
        await order_service.delete_order_by_id(order_id)
        return {"message": "Order successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}/item/{item_id}")
async def delete_item_from_order(order_id: int, item_id: int):
    try:
        await order_service.delete_item_from_order(order_id, item_id)
        return {"message": f"Item {item_id} removed from order {order_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))