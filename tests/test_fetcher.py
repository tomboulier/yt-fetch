"""Tests for yt_fetch.fetcher."""

from unittest.mock import MagicMock, patch

from yt_fetch.fetcher import extract_video_id, get_metadata, get_transcript


class TestExtractVideoId:
    def test_standard_url(self):
        assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_short_url(self):
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_shorts_url(self):
        assert extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_embed_url(self):
        assert extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_url_with_extra_params(self):
        assert (
            extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s") == "dQw4w9WgXcQ"
        )

    def test_invalid_url_returns_none(self):
        assert extract_video_id("https://example.com/not-a-video") is None

    def test_empty_string_returns_none(self):
        assert extract_video_id("") is None


class TestGetTranscript:
    def test_returns_transcript_text(self):
        mock_entry = MagicMock()
        mock_entry.text = "Hello world"
        mock_fetched = [mock_entry]

        mock_api = MagicMock()
        mock_api.fetch.return_value = mock_fetched

        with patch("yt_fetch.fetcher.YouTubeTranscriptApi", return_value=mock_api):
            result = get_transcript("dQw4w9WgXcQ")

        assert result == "Hello world"

    def test_falls_back_to_any_language(self):
        mock_entry = MagicMock()
        mock_entry.text = "Bonjour"
        mock_fetched = [mock_entry]

        mock_transcript = MagicMock()
        mock_transcript.fetch.return_value = mock_fetched

        mock_api = MagicMock()
        mock_api.fetch.side_effect = Exception("Language not available")
        mock_api.list.return_value = iter([mock_transcript])

        with patch("yt_fetch.fetcher.YouTubeTranscriptApi", return_value=mock_api):
            result = get_transcript("dQw4w9WgXcQ")

        assert result == "Bonjour"

    def test_returns_error_message_on_failure(self):
        with patch(
            "yt_fetch.fetcher.YouTubeTranscriptApi", side_effect=Exception("boom"), create=True
        ):
            result = get_transcript("dQw4w9WgXcQ")

        assert result.startswith("[Transcript unavailable:")


class TestGetMetadata:
    def test_returns_parsed_metadata(self):
        fake_meta = {
            "title": "My Video",
            "channel": "My Channel",
            "upload_date": "20240101",
            "description": "A description",
        }

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = __import__("json").dumps(fake_meta)

        with patch("yt_fetch.fetcher.subprocess.run", return_value=mock_result):
            result = get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result["title"] == "My Video"
        assert result["channel"] == "My Channel"
        assert result["upload_date"] == "2024-01-01"

    def test_formats_upload_date(self):
        fake_meta = {"title": "", "channel": "", "upload_date": "20260310", "description": ""}

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = __import__("json").dumps(fake_meta)

        with patch("yt_fetch.fetcher.subprocess.run", return_value=mock_result):
            result = get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result["upload_date"] == "2026-03-10"

    def test_returns_empty_dict_on_failure(self):
        with patch("yt_fetch.fetcher.subprocess.run", side_effect=Exception("yt-dlp not found")):
            result = get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result == {"title": "", "channel": "", "upload_date": "", "description": ""}

    def test_returns_empty_dict_when_yt_dlp_fails(self):
        mock_result = MagicMock()
        mock_result.returncode = 1

        with patch("yt_fetch.fetcher.subprocess.run", return_value=mock_result):
            result = get_metadata("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result == {"title": "", "channel": "", "upload_date": "", "description": ""}
