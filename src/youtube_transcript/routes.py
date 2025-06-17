from typing import Annotated
from fastapi import APIRouter, Depends

from src.youtube_transcript.services import YouTubeTranscriptService

router = APIRouter(
    prefix="/youtube-transcript",
    tags=["YouTube Transcript"],
)


@router.get("/{video_id}")
def get_youtube_transcript(
    video_id: str,
    youtube_transcript_service: Annotated[YouTubeTranscriptService, Depends()],
):
    """
    Fetch the transcript for a given YouTube video ID.
    """
    transcript = youtube_transcript_service.get_transcript(video_id)
    return {"video_id": video_id, "transcript": transcript}
