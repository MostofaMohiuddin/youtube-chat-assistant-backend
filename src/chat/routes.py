from typing import Annotated
from fastapi import APIRouter, Depends

from src.chat.dtos import ChatRequest, ChatResponse
from src.chat.services import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
def chat(
    chat_request: ChatRequest, chat_service: Annotated[ChatService, Depends()]
) -> ChatResponse:
    """
    Process a chat message.
    """
    # Here you would typically call a service to process the chat message
    # For now, we will just return the message back
    print("Received chat request:", chat_request.messages)
    print("Context:", chat_request.context)
    return chat_service.process_chat(chat_request)
