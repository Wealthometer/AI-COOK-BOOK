import os
import sys
import time
from openai import OpenAI
from openai.types import Video


def download_sora_video(
    video: Video,
    output_folder: str,
    filename: str = None,
    extension: str = ".mp4",
) -> Video:
    openai = OpenAI()
    progress = getattr(video, "progress", 0)
    bar_length = 30

    if filename is None:
        filename = video.id

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = f"{output_folder}/{filename}{extension}"

    while video.status in ("in_progress", "queued"):
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0)

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        status_text = "Queued" if video.status == "queued" else "Processing"

        sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
        sys.stdout.flush()
        time.sleep(2)

    sys.stdout.write("\n")

    if video.status == "failed":
        message = getattr(
            getattr(video, "error", None), "message", "Video generation failed"
        )
        print(message)
        sys.exit(1)

    print("Video generation completed:", video)
    print("Downloading video content...")

    content = openai.videos.download_content(video.id, variant="video")
    content.write_to_file(output_path)

    print(f"Wrote {output_path}")

    return video
