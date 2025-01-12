import json
import logging
from datetime import date
from typing import Optional, List, Dict

from model.item import Item
from model.order import Order
from model.order_item import OrderItem
from model.order_item_detail import OrderItemDetail
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from repository import order_repository, item_repository, user_repository, order_item_repository
from service import item_service


async def compute_total_price(item_quantities: Dict[int, int]) -> float:
    total_price = 0
    for item_id, quantity in item_quantities.items():
        item = await item_repository.get_item_by_id(item_id)
        if item:
            total_price += item.price * quantity
    return total_price


async def get_order_by_id(order_id: int) -> Optional[OrderResponse]:
    order = await order_repository.get_order_by_id(order_id)
    if not order:
        return None

    order_items = await order_item_repository.get_order_items_by_order_id(order_id)
    items = []
    total_price = 0

    for order_item in order_items:
        item = await item_service.get_item_by_id(order_item.item_id)
        if not item:
            raise ValueError(f"Item with ID {order_item.item_id} not found.")
        items.append(OrderItemDetail(
            item_id=item.id,
            name=item.name,
            price=item.price,
            quantity=order_item.quantity,
            item_stock=item.item_stock
        ))
        total_price += item.price * order_item.quantity

    order_response = OrderResponse(
        id=order.id,
        item=items,
        total_price=total_price,
        shipping_address=order.shipping_address,
        order_date=order.order_date,
        status=order.status
    )
    return order_response


async def get_order_by_user_id(user_id: int) -> List[OrderResponse]:
    user_order = await order_repository.get_order_by_user_id(user_id)
    if not user_order:
        return []

    response = []

    for order in user_order:
        order_items = await order_item_repository.get_order_items_by_order_id(order.id)
        items = []
        total_price = 0

        for order_item in order_items:
            item = await item_service.get_item_by_id(order_item.item_id)
            if not item:
                raise ValueError(f"Item with ID {order_item.item_id} not found.")

            items.append(OrderItemDetail(
                item_id=item.id,
                name=item.name,
                price=item.price,
                quantity=order_item.quantity,
                item_stock=item.item_stock
            ))

            total_price += item.price * order_item.quantity

        response.append(
            OrderResponse(
                id=order.id,
                item=items,
                total_price=total_price,
                shipping_address=order.shipping_address,
                order_date=order.order_date,
                status=order.status
            )
        )
    return response


# async def get_order_by_order_and_user_id(order_id: int, user_id: int) -> Optional[Dict]:
#     order = await order_repository.get_order_by_order_and_user_id(order_id, user_id)
#     if not order:
#         return None
#
#     items_list = []
#     total_price = 0
#
#     for item_id, quantity in order["item_quantities"].items():
#         item_details = await item_service.get_item_by_id(item_id)
#         if not item_details:
#             raise ValueError(f"Item with ID {item_id} not found")
#         items_list.append({
#             "name": item_details.name,
#             "price": item_details.price,
#             "item_stock": item_details.item_stock,
#             "quantity": quantity
#         })
#         total_price += item_details.price * quantity
#
#     order_response = OrderResponse(
#         order_id=order.id,
#         item=items_list,
#         total_price=total_price,
#         shipping_address=order.shipping_address,
#         status=order.status
#     )
#     return order_response


async def get_temp_order_by_user_id(user_id: int) -> Optional[OrderResponse]:
    temp_order = await order_repository.get_temp_order_by_user_id(user_id)
    if not temp_order:
        return None

    order_items = await order_item_repository.get_order_items_by_order_id(temp_order.id)
    items = []
    total_price = 0

    for order_item in order_items:
        item = await item_service.get_item_by_id(order_item.item_id)
        if not item:
            raise ValueError(f"Item with ID {order_item.item_id} not found.")

        items.append(OrderItemDetail(
                item_id=item.id,
                name=item.name,
                price=item.price,
                quantity=order_item.quantity,
                item_stock=item.item_stock
            ))
        total_price += item.price * order_item.quantity

    order_response = OrderResponse(
        id=temp_order.id,
        item=items,
        total_price=total_price,
        shipping_address=temp_order.shipping_address,
        order_date=temp_order.order_date,
        status=temp_order.status
    )
    return order_response


async def get_all_orders() -> List[Order]:
    return await order_repository.get_all_orders()


async def create_order(order_request: OrderRequest) -> None:
    try:
        user = await user_repository.get_user_by_id(order_request.user_id)
        if not user:
            raise ValueError("User does not exist or is not logged in.")

        existing_order = await order_repository.get_temp_order_by_user_id(order_request.user_id)
        if existing_order and existing_order.status == 'TEMP':
            raise ValueError("You already have an open order.")

        total_price = await compute_total_price(order_request.item_quantities)

        order = Order(
            user_id=order_request.user_id,
            order_date=date.today(),
            shipping_address=user.address,
            total_price=total_price,
            status=order_request.status
        )
        order_id = await order_repository.create_order(order)

        if not order_id:
            raise ValueError("Failed to create order in the database.")

        for item_id, quantity in order_request.item_quantities.items():
            order_item = OrderItem(order_id=order_id, item_id=item_id, quantity=quantity)
            await order_item_repository.create_order_items(order_item)

    except Exception as e:
        raise ValueError(f"Failed to create order: {e}")


async def update_order(order_id: int, order_request: OrderRequest):
    user = await user_repository.get_user_by_id(order_request.user_id)
    if not user:
        raise ValueError("User does not exist or is not logged in.")

    order = await order_repository.get_order_by_id(order_id)
    if not order:
        raise Exception(f"Can't update order. Order id '{order.id}' not found.")

    if order.status == OrderStatus.CLOSE:
        raise ValueError("Cannot update a closed order.")

    total_price = await compute_total_price(order_request.item_quantities)

    updated_order = Order(
        user_id=order_request.user_id,
        order_date=date.today(),
        shipping_address=order_request.shipping_address,
        total_price=total_price,
        status=order_request.status
    )
    await order_repository.update_order(order_id, updated_order)

    for item_id, quantity in order_request.item_quantities.items():
        existing_item = await order_item_repository.get_order_item(order_id, item_id)
        order_item = OrderItem(order_id=order_id, item_id=item_id, quantity=quantity)
        if existing_item:
            if quantity == 0:
                await delete_item_from_order(order_id, item_id)
            await order_item_repository.update_order_item(order_id, order_item)
        else:
            await order_item_repository.create_order_items(order_item)


async def update_temp_order(user_id: int, item_id: int, quantity: int):
    temp_order = await order_repository.get_temp_order_by_user_id(user_id)
    print(f"temp_order: {temp_order}")
    if not temp_order:
        raise ValueError("TEMP Order not found")

    if quantity == 0:
        await order_item_repository.delete_order_item(temp_order.id, item_id)
    else:
        order_item = OrderItem(order_id=temp_order.id, item_id=item_id, quantity=quantity)
        existing_item = await order_item_repository.get_order_item(temp_order.id, item_id)
        if existing_item:
            await order_item_repository.update_order_item(temp_order.id, order_item)
        else:
            await order_item_repository.create_order_items(order_item)

    order_items = await order_item_repository.get_order_items_by_order_id(temp_order.id)
    updated_item_quantities = {item.item_id: item.quantity for item in order_items}
    total_price = await compute_total_price(updated_item_quantities)

    await order_repository.update_temp_order(temp_order.id, total_price)


async def update_order_status(order_id: int, user_id: int, shipping_address: str, status: OrderStatus):
    temp_order = await get_temp_order_by_user_id(user_id)
    print(f"Temp order fetched service: {temp_order}")
    if not temp_order:
        raise ValueError(f"Open order with ID {user_id} not found")

    date_close = date.today()
    print(f"Date to close order: {date_close}")

    if status == OrderStatus.CLOSE:
        order_items = await order_item_repository.get_order_items_by_order_id(order_id)
        under_stock_item = []
        updated_items = []

        for order_item in order_items:
            item_data = await item_repository.get_item_by_id(order_item.item_id)
            if not item_data:
                raise ValueError(f"Item with ID {order_item.item_id} not found")

            if order_item.quantity > item_data.item_stock:
                under_stock_item.append(
                    {"item_id": item_data.id, "item_name": item_data.name, "required": order_item.quantity,
                     "available": item_data.item_stock}
                )
            else:
                new_stock = item_data.item_stock - order_item.quantity
                # if new_stock < 0:
                #     raise ValueError(f"Insufficient stock for item '{item_data.name}'")
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

        await order_repository.update_order_status(order_id, shipping_address, status, date_close)


async def delete_order_by_id(order_id: int):
    await order_repository.delete_order_by_id(order_id)
    await order_item_repository.delete_all_order_items(order_id)


async def delete_item_from_order(order_id: int, item_id: int):
    await order_item_repository.delete_order_item(order_id, item_id)
    # order = await order_repository.get_order_by_id(order_id)
    # if not order:
    #     raise Exception(f"Order with ID {order_id} does not exist")
    #
    # updated_item_quantities = {
    #     key: value for key, value in order.item_quantities.items() if key != item_id
    # }
    # print(f"updated_item_quantities before: {updated_item_quantities}")
    # if len(updated_item_quantities) == len(order.item_quantities):
    #     raise Exception(f"Item with ID {item_id} does not exist in the order")
    #
    # total_price = 0
    # for id_key, quantity in updated_item_quantities.items():
    #     item = await item_repository.get_item_by_id(int(id_key))
    #     if item:
    #         total_price += item.price * quantity
    #
    # await order_repository.update_temp_order(
    #     order_id=order.id,
    #     item_quantities=updated_item_quantities,
    #     total_price=total_price
    # )
