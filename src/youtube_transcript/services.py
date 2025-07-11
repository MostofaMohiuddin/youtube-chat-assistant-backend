from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from src.common.exceptions import NotFoundException
from src.youtube_transcript.repository import YouTubeTranscriptRepository


class YouTubeTranscriptService:
    def __init__(self):
        self.youtube_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username="cfkmhxhr",
                proxy_password="khlk2uo7n1kg",
            )
        )
        self.youtube_transcript_repository = YouTubeTranscriptRepository()

    def _fetch_transcript(self, video_id: str) -> list[dict]:
        """
        Fetch the transcript for a given YouTube video ID using YouTubeTranscriptApi.
        :param video_id: The ID of the YouTube video.
        :return: Transcript as a list of dictionaries.
        """
        try:
            print(f"Fetching transcript for video ID: {video_id}")
            return self.youtube_api.fetch(video_id).to_raw_data()
        except Exception as e:
            raise ValueError(
                f"Error fetching transcript for video ID {video_id}: {str(e)}"
            ) from e

    def _get_cached_transcript(self, video_id: str):
        """
        Fetch the transcript for a given YouTube video ID from the cache.
        :param video_id: The ID of the YouTube video.
        :return: Cached transcript as a list of dictionaries or None if not found.
        """
        try:
            # Check if the transcript is cached
            cached_transcript = self.youtube_transcript_repository.get_transcript(
                video_id
            )
            if cached_transcript:
                return cached_transcript
        except NotFoundException:
            print(f"Cached transcript not found for video ID: {video_id}")

    def get_transcript(self, video_id: str):
        """
        Fetch the transcript for a given YouTube video ID.
        :param video_id: The ID of the YouTube video.
        :return: Transcript as a list of dictionaries.
        """
        # try to fetch from cache
        cached_transcript = self._get_cached_transcript(video_id)
        if cached_transcript:
            print(f"Using cached transcript for video ID: {video_id}")
            return cached_transcript

        # If not cached, fetch from YouTube API
        transcript = self._fetch_transcript(video_id)
        if not transcript:
            raise NotFoundException(f"Transcript not found for video ID: {video_id}")
        # Save the transcript to cache
        self.youtube_transcript_repository.save_transcript(video_id, transcript)
        return transcript
