from src.chat.dtos import ChatRequest, ChatResponse
from src.common.exceptions import BadRequestException
from src.llm.service import LLMService
from src.youtube_transcript.services import YouTubeTranscriptService


class ChatService:
    """
    Service class for handling chat-related operations.
    """

    def __init__(self):
        self.youtube_transcript_service = (
            YouTubeTranscriptService()
        )  # Assuming LLMService is defined elsewhere

    def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        """
        Process a chat message and return a response.
        """
        context = chat_request.context
        messages = chat_request.messages
        llm_service = LLMService(api_key=chat_request.api_key)

        video_id = context.get("videoId")
        if not video_id:
            raise BadRequestException("videoId is required in context")
        transcript = self.youtube_transcript_service.get_transcript(video_id)
        response = llm_service.get_completion_for_youtube_transcript(
            transcript=transcript, messages=messages
        )
        return ChatResponse(message=response)
