"""CLI entry point for yt-fetch."""

import argparse
import json
import sys

from yt_fetch.fetcher import extract_video_id, get_metadata, get_transcript


def main() -> None:
    """Fetch YouTube metadata and transcript, output as JSON.

    Usage:
        yt-fetch https://www.youtube.com/watch?v=VIDEO_ID
    """
    parser = argparse.ArgumentParser(
        prog="yt-fetch",
        description="Fetch YouTube video metadata and transcript as JSON.",
    )
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(f"Error: cannot extract video ID from URL: {args.url}", file=sys.stderr)
        sys.exit(1)

    metadata = get_metadata(args.url)
    transcript = get_transcript(video_id)

    result = {
        "video_id": video_id,
        "url": args.url,
        "title": metadata["title"],
        "channel": metadata["channel"],
        "upload_date": metadata["upload_date"],
        "transcript": transcript,
    }

    print(json.dumps(result, ensure_ascii=False))
