from fastapi import APIRouter, Depends

from src.chat.dtos import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
def chat(chat_request: ChatRequest) -> ChatResponse:
    """
    Process a chat message.
    """
    # Here you would typically call a service to process the chat message
    # For now, we will just return the message back
    print("Received chat request:", chat_request.messages)
    print("Context:", chat_request.context)
    return ChatResponse(message="message")
