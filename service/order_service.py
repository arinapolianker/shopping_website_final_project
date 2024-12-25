import json
import logging
from datetime import date
from typing import Optional, List, Dict

from model.item import Item
from model.order import Order
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from repository import order_repository, item_repository, user_repository
from service import item_service


async def compute_total_price(item_quantities: dict):
    total_price = 0
    for item_id, quantity in item_quantities.items():
        item = await item_repository.get_item_by_id(item_id)
        if item:
            total_price += item.price * quantity
    return total_price


async def get_order_by_id(order_id: int) -> Optional[List[OrderResponse]]:
    order = await order_repository.get_order_by_id(order_id)
    if not order:
        return None

    response = []
    for item_id, quantity in order.item_quantities.items():
        item_details = await item_repository.get_item_by_id(int(item_id))
        if not item_details:
            raise ValueError(f"Item with ID {item_id} not found")
        order_response = OrderResponse(
            order_id=order.id,
            item=item_details,
            item_quantities={item_id: quantity},
            total_price=item_details.price * quantity,
            shipping_address=order.shipping_address,
            status=order.status
        )
        response.append(order_response)
    return response


async def get_order_by_user_id(user_id: int) -> List[OrderResponse]:
    user_order = await order_repository.get_order_by_user_id(user_id)
    if not user_order:
        return []

    response = []
    for order in user_order:
        for item_id, quantity in order.item_quantities.items():
            item_details = await item_service.get_item_by_id(item_id)
            if not item_details:
                raise ValueError(f"Item with ID {item_id} not found")

            order_response = OrderResponse(
                    item=item_details,
                    item_quantities={item_id: quantity},
                    total_price=item_details.price * quantity,
                    shipping_address=order.shipping_address,
                    status=order.status
                )
            response.append(order_response)

        return response


async def get_temp_order_by_user_id(user_id: int) -> Optional[Order]:
    user = await user_repository.get_user_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")

    open_order = await order_repository.get_temp_order_by_user_id(user_id)
    if open_order:
        return Order(**open_order)

    new_order = Order(
        user_id=user_id,
        order_date=date.today(),
        shipping_address=user.address,
        item_quantities={},
        total_price=0.0,
        status=OrderStatus.TEMP
    )
    order_id = await order_repository.create_order(new_order)
    new_order.id = order_id
    return new_order


async def update_temp_order(user_id: int, item_id: int, quantity: int):
    temp_order = await order_repository.get_temp_order_by_user_id(user_id)
    if not temp_order:
        raise ValueError("Order not found")

    item_quantities = json.loads(temp_order["item_quantities"]) if temp_order["item_quantities"] else {}
    if item_id in item_quantities:
        item_quantities[item_id] += quantity
    else:
        item_quantities[item_id] = quantity

    total_price = await compute_total_price(item_quantities)
    await order_repository.update_temp_order(temp_order["id"], item_quantities, total_price)


async def get_all_orders() -> List[Order]:
    return await order_repository.get_all_orders()


async def create_order(order_request: OrderRequest) -> Optional[int]:
    try:
        user = await user_repository.get_user_by_id(order_request.user_id)
        if not user:
            raise ValueError("User does not exist or is not logged in.")

        existing_order = await order_repository.get_temp_order_by_user_id(order_request.user_id)
        if existing_order and existing_order['status'] == 'TEMP':
            raise ValueError("You already have an open order.")

        if isinstance(order_request.item_quantities, str):
            item_quantities = json.loads(order_request.item_quantities)
        else:
            item_quantities = order_request.item_quantities

        total_price = await compute_total_price(item_quantities)

        order = Order(
            user_id=order_request.user_id,
            order_date=date.today(),
            shipping_address=user.address if user else "",
            item_quantities=item_quantities,
            total_price=total_price,
            status=order_request.status
        )

        order_id = await order_repository.create_order(order)
        if not order_id:
            raise ValueError("Failed to create the order.")

    except Exception as e:
        raise ValueError(f"Failed to create order: {e}")


async def update_order(order_id: int, order_request: OrderRequest):
    user = await user_repository.get_user_by_id(order_request.user_id)

    if not user:
        raise ValueError("User does not exist or is not logged in.")

    order = await order_repository.get_order_by_id(order_id)
    if not order.id:
        raise Exception(f"Can't update order. Order id '{order.id}' not found.")

    if order.status != OrderStatus.CLOSE and order_request.status != OrderStatus.CLOSE:
        if isinstance(order_request.item_quantities, str):
            item_quantities = json.loads(order_request.item_quantities)
        else:
            item_quantities = order_request.item_quantities

        total_price = await compute_total_price(item_quantities)

        updated_order = Order(
            user_id=order_request.user_id,
            order_date=date.today(),
            shipping_address=user.address if user else "",
            item_quantities=item_quantities,
            total_price=total_price,
            status=order_request.status
        )
        await order_repository.update_order(order_id, updated_order)


async def update_order_status(order_id: int, status: OrderStatus):
    order = await order_repository.get_order_by_id(order_id)
    if not order:
        raise ValueError(f"Order with ID {order_id} not found")

    if status == OrderStatus.CLOSE:
        under_stock_item = []
        updated_items = []

        for item_id, quantity in order.item_quantities.items():
            item_data = await item_repository.get_item_by_id(item_id)
            if not item_data:
                raise ValueError(f"Item with ID {item_id} not found")

            if quantity > item_data.item_stock:
                under_stock_item.append(
                    {"item_id": item_id, "item_name": item_data.name, "required": quantity,
                     "available": item_data.item_stock}
                )
            else:
                new_stock = item_data.item_stock - quantity
                if new_stock < 0:
                    raise ValueError(f"Insufficient stock for item '{item_data.name}'")
                updated_items.append(
                    Item(
                        id=item_data.id,
                        name=item_data.name,
                        price=item_data.price,
                        item_stock=new_stock
                    )
                )
        if under_stock_item:
            raise ValueError(f"Insufficient stock for items: {under_stock_item}")

        for updated_item in updated_items:
            await item_repository.update_item(updated_item.id, updated_item)

        await order_repository.update_order_status(order_id, status)


async def delete_order_by_id(order_id: int):
    await order_repository.delete_order_by_id(order_id)


async def delete_order_by_user_id(user_id: int):
    await order_repository.delete_order_by_user_id(user_id)


async def delete_item_from_order(order_id: int, item_id: int):
    order = await order_repository.get_order_by_id(order_id)
    if not order:
        raise Exception(f"Order with ID {order_id} does not exist")

    updated_item_quantities = {
        key: value for key, value in order.item_quantities.items() if key != item_id
    }

    if len(updated_item_quantities) == len(order.item_quantities):
        raise Exception(f"Item with ID {item_id} does not exist in the order")

    total_price = 0
    for id_key, quantity in updated_item_quantities.items():
        item = await item_repository.get_item_by_id(int(id_key))
        if item:
            total_price += item.price * quantity

    await order_repository.update_temp_order(
        order_id=order.id,
        item_quantities=updated_item_quantities,
        total_price=total_price
    )
