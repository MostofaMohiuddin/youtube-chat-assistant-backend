from enum import Enum
from pydantic import BaseModel


class ChatMessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    content: str
    role: ChatMessageRole


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: dict = {}


class ChatResponse(BaseModel):
    message: str
