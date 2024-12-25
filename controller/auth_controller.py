from starlette import status

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from exceptions.security_exceptions import user_credentials_exception
from model.auth_response import AuthResponse
from service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise user_credentials_exception()
    return auth_service.create_access_token(user.username, user.id)
    # access_token = auth_service.create_access_token(user.username, user.id)
    # return {"jwt_token": access_token, "user_id": user.id}

# @router.post("/token", status_code=status.HTTP_200_OK, response_model=AuthResponse)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     try:
#         user = await auth_service.authenticate_user(form_data.username, form_data.password)
#         if not user:
#             raise user_credentials_exception()
#         access_token = auth_service.create_access_token(user.username, user.id)
#         return {"jwt_token": access_token, "user_id": user.id}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal Server Error")
