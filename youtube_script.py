import os
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime

OUTPUT_FILE = "playlist_transcripts.txt"


def get_playlist_videos(playlist_url):
    """
    Extract all videos from playlist.
    """

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(
            playlist_url,
            download=False
        )

    videos = []

    for entry in playlist_info["entries"]:
        videos.append({
            "id": entry["id"],
            "title": entry["title"],
            "url": f"https://www.youtube.com/watch?v={entry['id']}"
        })

    return videos


def get_transcript(video_id):
    """
    Fetch transcript.
    """

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        full_text = " ".join(
            item["text"] for item in transcript
        )

        return full_text

    except Exception as e:
        return f"Transcript unavailable: {e}"


def save_playlist_transcripts(
        playlist_url,
        output_file=OUTPUT_FILE
):
    videos = get_playlist_videos(playlist_url)

    with open(
            output_file,
            "w",
            encoding="utf-8"
    ) as f:

        f.write("=" * 100 + "\n")
        f.write("YOUTUBE PLAYLIST TRANSCRIPT EXPORT\n")
        f.write("=" * 100 + "\n\n")

        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Videos Found: {len(videos)}\n\n")

        for idx, video in enumerate(videos, start=1):

            print(
                f"[{idx}/{len(videos)}] "
                f"Processing: {video['title']}"
            )

            transcript = get_transcript(
                video["id"]
            )

            f.write("\n")
            f.write("#" * 100 + "\n")
            f.write(f"VIDEO {idx}\n")
            f.write("#" * 100 + "\n")

            f.write(
                f"Title: {video['title']}\n"
            )

            f.write(
                f"URL: {video['url']}\n\n"
            )

            f.write("TRANSCRIPT\n")
            f.write("-" * 80 + "\n")
            f.write(transcript)
            f.write("\n\n")

    print(
        f"\nCompleted.\nSaved: {output_file}"
    )


if __name__ == "__main__":

    playlist_url = input(
        "Enter YouTube Playlist URL: "
    )

    save_playlist_transcripts(
        playlist_url
    )