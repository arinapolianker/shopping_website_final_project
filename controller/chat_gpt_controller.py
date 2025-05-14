from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from api.externalApi.chatGPT import chat_gpt_api
from exceptions.security_exceptions import token_exception
from model.chat_gpt_request import ChatRequest
from service import auth_service
from service.auth_service import oauth2_bearer

router = APIRouter(
    prefix="/chat_gpt",
    tags=['chat_gpt']
)

user_question_count = {}


@router.post("/", status_code=status.HTTP_200_OK)
async def get_answer(chat_req: ChatRequest, token: str = Depends(oauth2_bearer)):
    user_response = await auth_service.validate_user(token)
    if user_response is None:
        raise token_exception()
    user_question_count.setdefault(chat_req.user_id, 0)
    user_question_count[chat_req.user_id] += 1
    if user_question_count[chat_req.user_id] > 5:
        raise HTTPException(status_code=429, detail="Limit reached: 5 questions allowed per session.")
    # if user_question_count[chat_req.user_id] >= 5:
    #     raise HTTPException(status_code=429, detail="Limit reached: 5 questions allowed per session.")
    # user_question_count[chat_req.user_id] += 1
    return await chat_gpt_api.get_answer(chat_req.question, chat_req.user_id)
