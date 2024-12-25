from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from exceptions.security_exceptions import token_exception
from model.user_request import UserRequest
from model.user_response import UserResponse
from service import auth_service, user_service

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={401: {"user": "Not authorized"}}
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    else:
        return await user_service.get_user_by_id(user_response.id)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    return await user_service.get_all_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: UserRequest):
    try:
        return await user_service.create_user(user_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_id(user_id: int, user: UserRequest, token: str = Depends(oauth2_bearer)):
    user_exists = await user_service.get_user_by_id(user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail=f"Can't update user with id:{user_id}, user not found...")
    await user_service.update_user_by_id(user_id, user, token)
    return await user_service.get_user_by_id(user_id)


@router.put("/log/{user_id}", response_model=UserResponse)
async def log_user_by_id(user_id: int):
    user_exists = await user_service.get_user_by_id(user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail=f"Can't register user with id:{user_id}, user not found...")
    await user_service.log_user_by_id(user_id)
    return await user_service.get_user_by_id(user_id)


@router.delete("/{user_id}")
async def delete_user_by_id(user_id: int):
    user_exists = await user_service.get_user_by_id(user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail=f"Can't delete user with id:{user_id}, user not found...")
    await user_service.delete_user_by_id(user_id)

