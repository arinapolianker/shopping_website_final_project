from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    user_id: int
