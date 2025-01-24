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
    return Order(**result) if result else None


async def get_order_by_user_id(user_id: int) -> List[Order]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE user_id=:user_id"
    results = await database.fetch_all(query, values={"user_id": user_id})
    return [Order(**result) for result in results]


async def get_temp_order_by_user_id(user_id: int) -> Optional[Order]:
    query = f"""
            SELECT * FROM {TABLE_NAME}
            WHERE user_id = :user_id AND status = 'TEMP'
            ORDER BY order_date DESC LIMIT 1
        """
    result = await database.fetch_one(query, values={"user_id": user_id})
    return Order(**result) if result else None


async def get_all_orders() -> List[Order]:
    query = f"SELECT * FROM {TABLE_NAME}"
    results = await database.fetch_all(query)
    return [Order(**result) for result in results]


async def create_order(order: Order) -> Optional[int]:
    query = f"""
        INSERT INTO {TABLE_NAME} (user_id, order_date, shipping_address, total_price, status)
        VALUES (:user_id, :order_date, :shipping_address, :total_price, :status)
    """
    values = {
        "user_id": order.user_id,
        "order_date": order.order_date,
        "shipping_address": order.shipping_address,
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
        total_price = :total_price,
        status = :status
        WHERE id = :order_id
    """
    values = {
        "order_id": order_id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "shipping_address": order.shipping_address,
        "total_price": order.total_price,
        "status": order.status.value
    }
    await database.execute(query, values)


async def update_temp_order(order_id: int, total_price: float):
    query = f"""
        UPDATE {TABLE_NAME}
        SET total_price = :total_price
        WHERE id = :order_id AND status = 'TEMP'
    """
    values = {
        "total_price": total_price,
        "order_id": order_id
    }
    await database.execute(query, values)


async def update_order_status(order_id: int, shipping_address: str, status: OrderStatus, date_close: date):
    query = f"""
        UPDATE {TABLE_NAME}
        SET order_date = :order_date, shipping_address = :shipping_address, status = :status
        WHERE id = :order_id
    """
    values = {
        "order_id": order_id,
        "order_date": date_close.isoformat(),
        "shipping_address": shipping_address,
        "status": status.value
    }
    await database.execute(query, values)



async def delete_order_by_id(order_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE id=:order_id"
    await database.execute(query, values={"order_id": order_id})


async def delete_order_by_user_id(user_id: int):
    query = f"DELETE FROM {TABLE_NAME} WHERE user_id=:user_id"
    await database.execute(query, values={"user_id": user_id})

