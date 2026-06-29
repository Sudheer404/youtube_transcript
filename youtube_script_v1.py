import os
from datetime import datetime

from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi


OUTPUT_FILE = "playlist_transcripts.txt"


def get_playlist_videos(playlist_url):
    """
    Extract all videos from playlist
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

        if not entry:
            continue

        videos.append(
            {
                "id": entry.get("id"),
                "title": entry.get("title", "Unknown Title"),
                "url": f"https://www.youtube.com/watch?v={entry.get('id')}"
            }
        )

    return videos


def get_transcript(video_id):
    """
    Download transcript using youtube-transcript-api v1.2.4
    """

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = "\n".join(
            segment.text
            for segment in transcript
        )

        return text

    except Exception as first_error:

        try:

            api = YouTubeTranscriptApi()

            transcript_list = api.list(video_id)

            transcript = transcript_list.find_transcript(
                ["en"]
            )

            transcript_data = transcript.fetch()

            text = "\n".join(
                segment.text
                for segment in transcript_data
            )

            return text

        except Exception as second_error:

            return (
                f"Transcript unavailable\n"
                f"Primary Error : {first_error}\n"
                f"Fallback Error: {second_error}"
            )


def save_playlist_transcripts(
    playlist_url,
    output_file=OUTPUT_FILE
):

    videos = get_playlist_videos(playlist_url)

    print(f"\nFound {len(videos)} videos\n")

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("=" * 100 + "\n")
        f.write("YOUTUBE PLAYLIST TRANSCRIPT EXPORT\n")
        f.write("=" * 100 + "\n\n")

        f.write(
            f"Generated: {datetime.now()}\n"
        )

        f.write(
            f"Videos Found: {len(videos)}\n\n"
        )

        for index, video in enumerate(
            videos,
            start=1
        ):

            print(
                f"[{index}/{len(videos)}] "
                f"{video['title']}"
            )

            transcript_text = get_transcript(
                video["id"]
            )

            f.write("\n")
            f.write("#" * 100 + "\n")
            f.write(
                f"VIDEO {index}\n"
            )
            f.write("#" * 100 + "\n")

            f.write(
                f"Title: {video['title']}\n"
            )

            f.write(
                f"Video ID: {video['id']}\n"
            )

            f.write(
                f"URL: {video['url']}\n\n"
            )

            f.write(
                "TRANSCRIPT\n"
            )

            f.write(
                "-" * 80 + "\n"
            )

            f.write(transcript_text)

            f.write("\n\n")

    print("\nDone")
    print(
        f"Output File: "
        f"{os.path.abspath(output_file)}"
    )


if __name__ == "__main__":

    playlist_url = input(
        "\nEnter YouTube Playlist URL:\n"
    ).strip()

    save_playlist_transcripts(
        playlist_url
    )