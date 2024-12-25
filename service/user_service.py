from typing import Optional, List

from fastapi import HTTPException
from passlib.context import CryptContext

from exceptions.security_exceptions import username_taken_exception, token_exception
from model.user import User
from model.user_request import UserRequest
from model.user_response import UserResponse
from repository import user_repository
from service import order_service

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def validate_unique_username(username: str) -> bool:
    user_exists = await user_repository.get_user_by_username(username)
    return user_exists is None


async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    user = await user_repository.get_user_by_id(user_id)
    if user:
        return UserResponse(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
    else:
        return None


async def get_user_by_username(username: str) -> User:
    return await user_repository.get_user_by_username(username)


async def get_all_users() -> List[UserResponse]:
    users = await user_repository.get_all_users()
    return [UserResponse(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    ) for user in users]


async def create_user(user_request: UserRequest):
    if await validate_unique_username(user_request.username):
        hashed_password = get_password_hash(user_request.password)
        await user_repository.create_user(user_request, hashed_password)
    else:
        raise username_taken_exception()


async def update_user_by_id(user_id: int, user_request: UserRequest, token: str):
    updated_user = UserResponse(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        phone=user_request.phone,
        address=user_request.address,
        username=user_request.username
    )
    hashed_password = (
        get_password_hash(user_request.password)
        if user_request.password else None
    )
    await user_repository.update_user_by_id(user_id, user_request, hashed_password)
    return updated_user


async def update_user_by_username(username: str, user_request: UserRequest, token: str):
    updated_user = UserResponse(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        phone=user_request.phone,
        address=user_request.address,
        username=user_request.username
    )
    hashed_password = (
        get_password_hash(user_request.password)
        if user_request.password else None
    )
    await user_repository.update_user_by_username(username, user_request, hashed_password)
    return updated_user


async def log_user_by_id(user_id: int):
    user_exists = await user_repository.get_user_by_id(user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail=f"User with id:{user_id} not found.")
    if not user_exists.is_logged:
        return await user_repository.log_user_by_id(user_id, True)
    else:
        raise HTTPException(status_code=404, detail=f"User with id:{user_id} is already registered")


async def delete_user_by_id(user_id):
    user_orders = await order_service.get_order_by_user_id(user_id)
    if user_orders:
        orders_deleted = await order_service.delete_order_by_user_id(user_id)
        if orders_deleted:
            raise HTTPException(status_code=500, detail=f"Failed to delete orders for user_id: {user_id}.")
    await user_repository.delete_user_by_id(user_id)


async def delete_user_by_username(username):
    orders_deleted = await order_service.delete_order_by_user_id(username)
    if not orders_deleted:
        raise HTTPException(status_code=500, detail=f"Failed to delete orders for user_id: {user_id}.")
    await user_repository.delete_user_by_username(username)


