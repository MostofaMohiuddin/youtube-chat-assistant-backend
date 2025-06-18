from openai import OpenAI

from src.chat.dtos import ChatMessage
from src.llm.prompts import SYSTEM_PROMPT


class LLMService:
    def __init__(self, api_key: str = None):
        if api_key is None:
            raise ValueError("API key must be provided for LLMService")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def get_completion(
        self,
        messages: list[dict],
        model: str = "openai/gpt-4o",
    ):
        """
        Get a completion from the OpenAI API.

        Args:
            messages (list[dict]): List of messages for the chat.
            model (str): The model to use for the completion.
        Returns:
            str: The content of the completion response.
        """

        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return completion.choices[0].message.content

    def get_completion_for_youtube_transcript(
        self,
        messages: list[ChatMessage],
        transcript: list[dict],
        model: str = "openai/gpt-4o",
    ) -> str:
        """
        Get a completion for a YouTube transcript.

        Args:
            messages (list[ChatMessage]): List of chat messages.
            transcript (list[dict]): The transcript of the YouTube video.
            model (str): The model to use for the completion.
        Returns:
            str: The content of the completion response.
        """
        formatted_messages = [
            {"role": msg.role.value, "content": msg.content} for msg in messages
        ]
        system_prompt = (
            SYSTEM_PROMPT
            + f"""\n\n
        The transcript of the YouTube video is an array of dictionaries, where each dictionary contains 'text', 'start' and 'duration' keys. These keys represent the text of the transcript, the start time of the text in seconds, and the duration of the text in seconds respectively.

        Here is the transcript of the YouTube video:
        {transcript}
        """
        )
        system_message = {
            "role": "system",
            "content": system_prompt,
        }
        content = self.get_completion([system_message] + formatted_messages, model)
        return content
