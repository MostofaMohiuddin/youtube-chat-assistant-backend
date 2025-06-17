import json
from src.common.exceptions import NotFoundException
from src.common.redis.connection import RedisConnection


class YouTubeTranscriptRepository:
    def __init__(self):
        self.redis_client = RedisConnection.get_instance()

    def get_transcript(self, video_id: str) -> list:
        """
        Fetch the transcript for a given YouTube video ID from Redis.

        Args:
            video_id (str): The YouTube video ID.

        Returns:
            list: The transcript for the video.
        """
        transcript = self.redis_client.get(video_id)
        if transcript is None:
            raise NotFoundException(f"Transcript not found for video ID: {video_id}")
        return json.loads(transcript)

    def save_transcript(self, video_id: str, transcript: list) -> None:
        """
        Save the transcript for a given YouTube video ID to Redis.
        Args:
            video_id (str): The YouTube video ID.
            transcript (list): The transcript to save.
        """
        try:
            self.redis_client.set(video_id, json.dumps(transcript))
            print(f"Transcript for video ID {video_id} saved successfully.")
        except Exception as e:
            print(f"Error saving transcript for video ID {video_id}: {str(e)}")
            raise e
