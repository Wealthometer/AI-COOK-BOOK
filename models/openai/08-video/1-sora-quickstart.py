import sys
import time
from openai import OpenAI

openai = OpenAI()

# --------------------------------------------------------------
# Create a new video
# --------------------------------------------------------------

# Takes about 2 minutes
video = openai.videos.create(
    model="sora-2",
    prompt="YouTuber, black t-shirt, in a professional studio setup, sitting at his desk talking directly into a Shure SM7B microphone on a boom arm. He says with a smirk: 'Wait... did an AI just generate me to teach you about AI? That's pretty meta...' Dark background with a soft blue LED light glow. Professional lighting setup with key light and rim light. Shot on Sony FX6, cinematic depth of field, crisp focus, vertical format 9:16.",
    size="720x1280",
    seconds="4",
)

print("Video generation started:", video)

# --------------------------------------------------------------
# List all videos
# --------------------------------------------------------------

time.sleep(5)
videos_list = openai.videos.list().data

# --------------------------------------------------------------
# Check the last's video status
# --------------------------------------------------------------

video = openai.videos.retrieve(videos_list[0].id)
print("Video status:", video.status)

# --------------------------------------------------------------
# Download video
# --------------------------------------------------------------

progress = getattr(video, "progress", 0)
bar_length = 30

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
content.write_to_file(f"output/{video.id}.mp4")

print(f"Wrote output/{video.id}.mp4")
