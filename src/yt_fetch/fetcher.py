"""Core fetching logic: video ID extraction, metadata, transcript."""

import json
import re
import subprocess

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str | None:
    """Extract the YouTube video ID from a URL.

    Supports standard, short, embed, and shorts URL formats.

    Args:
        url: Any YouTube URL format.

    Returns:
        The 11-character video ID, or None if not found.

    Examples:
        >>> extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
        >>> extract_video_id("https://youtu.be/dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
        >>> extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
        >>> extract_video_id("not-a-url") is None
        True
    """
    patterns = [
        r"(?:v=|/watch\?v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"(?:embed/)([a-zA-Z0-9_-]{11})",
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id: str) -> str:
    """Fetch the transcript for a YouTube video.

    Tries French first, then English variants, then any available language.

    Args:
        video_id: The 11-character YouTube video ID.

    Returns:
        The full transcript as a single string, or an error message
        prefixed with '[Transcript unavailable: ...]' if fetching fails.
    """
    try:
        api = YouTubeTranscriptApi()
        try:
            fetched = api.fetch(video_id, languages=["fr", "en", "en-US", "en-GB"])
            return " ".join(t.text for t in fetched)
        except Exception:
            transcripts = api.list(video_id)
            transcript = next(iter(transcripts))
            fetched = transcript.fetch()
            return " ".join(t.text for t in fetched)
    except Exception as e:
        return f"[Transcript unavailable: {e}]"


def get_metadata(url: str) -> dict:
    """Fetch video metadata using yt-dlp.

    Args:
        url: The full YouTube URL.

    Returns:
        A dict with keys 'title', 'channel', 'upload_date', 'description'.
        Returns empty strings on failure.
    """
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-playlist", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            meta = json.loads(result.stdout)
            upload_date = meta.get("upload_date", "")
            if upload_date and len(upload_date) == 8:
                upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
            return {
                "title": meta.get("title", ""),
                "channel": meta.get("channel", meta.get("uploader", "")),
                "upload_date": upload_date,
                "description": meta.get("description", "")[:500],
            }
    except Exception:
        pass
    return {"title": "", "channel": "", "upload_date": "", "description": ""}
