import json
from typing import Optional, List

from model.user import User
from model.user_request import UserRequest
from repository import cache_repository
from repository.database import database

USER_TABLE_NAME = "users"


async def get_user_by_id(user_id: int) -> Optional[User]:
    query = f"SELECT * FROM {USER_TABLE_NAME} WHERE id=:user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return User(**result)
    else:
        return None


async def get_user_by_username(username: str) -> Optional[User]:
    if cache_repository.is_key_exists(str(username)):
        string_user = cache_repository.get_cache_entity(str(username))
        user_data = json.loads(string_user)
        if "hashed_password" not in user_data or "is_logged" not in user_data:
            print(f"Cache missing required fields for {username}, fetching from DB.")

        print(f"Cache Data for {username}: {user_data}")
        return User(**user_data)
    else:
        query = f"SELECT * FROM {USER_TABLE_NAME} WHERE username=:username"
        result = await database.fetch_one(query, values={"username": username})
        if result:
            user = User(**result)
            cache_repository.create_cache_entity(str(username), user.json())
            return user
        else:
            return None


async def get_all_users() -> List[User]:
    query = f"SELECT * FROM {USER_TABLE_NAME} WHERE is_logged=:is_logged"
    results = await database.fetch_all(query, values={"is_logged": True})
    return [User(**result) for result in results]


async def create_user(user: UserRequest, hashed_password: str):
    query = f"""
        INSERT INTO {USER_TABLE_NAME} (first_name, last_name, email, phone, address, username, hashed_password, is_logged)
        VALUES (:first_name, :last_name, :email, :phone, :address, :username, :hashed_password, :is_logged)
    """
    user_dict = user.dict()
    del user_dict["password"]
    values = {**user_dict, "hashed_password": hashed_password, "is_logged": True}
    user_dict["hashed_password"] = hashed_password
    user_dict["is_logged"] = True
    cache_repository.create_cache_entity(str(user.username), json.dumps(user_dict))
    await database.execute(query, values)


async def update_user_by_id(user_id: int, user: UserRequest, hashed_password: Optional[str] = None):
    query = f"""
        UPDATE {USER_TABLE_NAME} 
        SET first_name = :first_name,
        last_name = :last_name,
        email = :email,
        address = :address,
        username = :username,
        {", hashed_password = :hashed_password" if hashed_password else ""}
        WHERE id = :user_id
    """
    values = {
        "user_id": user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "username": user.username
    }
    if hashed_password:
        values["hashed_password"] = hashed_password

    await database.execute(query, values=values)


async def update_user_by_username(username: str, user: UserRequest, hashed_password: Optional[str] = None):
    if cache_repository.is_key_exists(str(username)):
        cache_repository.update_cache_entity(str(username), user.json())

    query = f"""
        UPDATE {USER_TABLE_NAME} 
        SET first_name = :first_name,
        last_name = :last_name,
        email = :email,
        address = :address,
        username = :username,
        {", hashed_password = :hashed_password" if hashed_password else ""}
        WHERE username = :username
    """
    values = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "username": username
    }
    if hashed_password:
        values["hashed_password"] = hashed_password

    await database.execute(query, values=values)


async def log_user_by_id(user_id: int, is_logged: bool):
    query = f"""
        UPDATE {USER_TABLE_NAME} 
        SET is_logged = :is_logged
        WHERE id = :user_id
    """
    values = {
        "user_id": user_id,
        "is_logged": is_logged
    }

    await database.execute(query, values=values)


async def delete_user_by_id(user_id: int):
    cache_repository.remove_cache_entity(str(user_id))
    query = f"DELETE FROM {USER_TABLE_NAME} WHERE id=:user_id"
    await database.execute(query, values={"user_id": user_id})


async def delete_user_by_username(username: str):
    cache_repository.remove_cache_entity(str(username))

    query = f"DELETE FROM {USER_TABLE_NAME} WHERE username=:username"
    await database.execute(query, values={"username": username})

