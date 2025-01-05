import logging
from datetime import date
from typing import List, Optional, Dict
import json

from model.order import Order
from model.order_response import OrderResponse
from model.order_status import OrderStatus
from repository.database import database

TABLE_NAME = "orders"


async def get_order_by_id(order_id: int) -> Optional[Order]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id=:order_id"
    result = await database.fetch_one(query, values={"order_id": order_id})
    return Order(**dict(result)) if result else None


async def get_order_by_user_id(user_id: int) -> List[Order]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id"
    results = await database.fetch_all(query, values={"user_id": user_id})
    orders = []
    for result in results:
        result = dict(result)
        item_quantities = result.get("item_quantities")
        if isinstance(item_quantities, str):
            result["item_quantities"] = json.loads(item_quantities)
        orders.append(Order(**result))
    return orders


async def get_order_by_order_and_user_id(order_id: int, user_id: int) -> Optional[Dict]:
    query = f"""
            SELECT * FROM {TABLE_NAME}
            WHERE id = :order_id AND user_id = :user_id
        """
    result = await database.fetch_one(query, values={"order_id": order_id, "user_id": user_id})
    if result:
        result_dict = dict(result)
        result_dict["item_quantities"] = json.loads(result_dict["item_quantities"])
        return result_dict
    return None


async def get_temp_order_by_user_id(user_id: int) -> Optional[Dict]:
    query = f"""
            SELECT * FROM {TABLE_NAME}
            WHERE user_id = :user_id AND status = 'TEMP'
            ORDER BY order_date DESC LIMIT 1
        """
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        result_dict = dict(result)
        result_dict["item_quantities"] = json.loads(result_dict["item_quantities"])
        return result_dict
    return None


async def update_temp_order(order_id: int, item_quantities: dict, total_price: float):
    query = f"""
        UPDATE {TABLE_NAME}
        SET item_quantities = :item_quantities, total_price = :total_price
        WHERE id = :order_id AND status = 'TEMP'
    """
    values = {
        "item_quantities": json.dumps(item_quantities),
        "total_price": total_price,
        "order_id": order_id
    }
    print(f"Executing query: {query} with values: {values}")
    await database.execute(query, values)


async def get_all_orders() -> List[Order]:
    query = f"SELECT * FROM {TABLE_NAME}"
    results = await database.fetch_all(query)
    return [Order(**result) for result in results]


async def create_order(order: Order) -> Optional[int]:
    query = f"""
        INSERT INTO {TABLE_NAME} (user_id, order_date, shipping_address, item_quantities, total_price, status)
        VALUES (:user_id, :order_date, :shipping_address, :item_quantities, :total_price, :status)
    """
    values = {
        "user_id": order.user_id,
        "order_date": order.order_date,
        "shipping_address": order.shipping_address,
        "item_quantities": json.dumps(order.item_quantities),
        "total_price": order.total_price,
        "status": order.status.value
    }

    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0] if last_record_id else None


async def update_order(order_id: int, order: Order):
    query = f"""
        UPDATE {TABLE_NAME}
        SET user_id = :user_id, 
        order_date = :order_date, 
        shipping_address = :shipping_address, 
        item_quantities = :item_quantities, 
        total_price = :total_price
        status = :status
        WHERE id = :order_id
    """
    values = {
        "order_id": order_id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "shipping_address": order.shipping_address,
        "item_quantities": json.dumps(order.item_quantities),
        "total_price": order.total_price,
        "status": order.status
    }
    await database.execute(query, values)
    await database.commit()


async def update_order_status(order_id: int, shipping_address: str, status: OrderStatus):
    query = f"""
        UPDATE {TABLE_NAME}
        SET shipping_address = :shipping_address, status = :status
        WHERE id = :order_id
    """
    values = {
        "order_id": order_id,
        "shipping_address": shipping_address,
        "status": status.value,
    }
    await database.execute(query, values)


async def delete_order_by_id(order_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE id=:order_id"
    await database.execute(query, values={"order_id": order_id})


async def delete_order_by_user_id(user_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE user_id=:user_id"
    await database.execute(query, values={"user_id": user_id})


# async def delete_items_from_order(order_id: int, item_id: int):
#     query = f"DELETE FROM {TABLE_NAME} WHERE status = 'TEMP'"
#     temp_orders = await database.fetch_all()
#     await database.execute(query, values={"item_id": item_id})

