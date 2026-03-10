# yt-fetch

A small personal utility that fetches YouTube video metadata and transcript as JSON from the command line.

```bash
yt-fetch https://www.youtube.com/watch?v=VIDEO_ID
```

```json
{
  "video_id": "VIDEO_ID",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "Video title",
  "channel": "Channel name",
  "upload_date": "2026-03-10",
  "transcript": "Full transcript text..."
}
```

## What this is

This is **glue code** between two excellent projects:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — for video metadata (title, channel, date)
- **[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)** — for transcript text

The value is in the single-command interface: one URL in, one clean JSON out. Useful for piping into LLMs, note-taking workflows, or any script that needs structured YouTube data.

It was built as part of a personal [Claude Code](https://claude.ai/code) + Obsidian workflow. Published here for personal reference and easy sharing — not as a serious library.

## Installation

```bash
pip install yt-fetch
```

Or with uv:

```bash
uv tool install yt-fetch
```

**Prerequisites:** `yt-dlp` must be installed and available in your PATH.

```bash
pip install yt-dlp
```

## Usage

```bash
# Basic usage
yt-fetch https://www.youtube.com/watch?v=VIDEO_ID

# Pipe to jq
yt-fetch https://youtu.be/VIDEO_ID | jq '.title'

# Save to file
yt-fetch https://www.youtube.com/watch?v=VIDEO_ID > video_data.json
```

## Development

```bash
# Install dependencies
make install

# Run tests
make test

# Lint and format
make check
make fmt
```

## License

MIT — see [LICENSE](LICENSE).
