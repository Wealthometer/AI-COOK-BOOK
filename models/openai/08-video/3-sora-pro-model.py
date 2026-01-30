from openai import OpenAI

from utils.downloader import download_sora_video

openai = OpenAI()

# --------------------------------------------------------------
# Generate a video with Sora Pro mode
# --------------------------------------------------------------

# Stays stuck in progress right now...
video = openai.videos.create(
    model="sora-2-pro",
    prompt="The YouTuber leans forward with an excited, intense expression while talking into the Shure SM7B. He says with energy: 'OpenAI just dropped Sora 2 via API... and honestly, this changes EVERYTHING. We're talking hyper-realistic videos with like 10 lines of code. Wild.' Dark background with a soft blue LED light glow. Professional lighting setup with key light and rim light. Shot on Sony FX6, cinematic depth of field, crisp focus, vertical format 9:16.",
    size="1024x1792",
    seconds="4",
)

print("Video generation started:", video)

# --------------------------------------------------------------
# Get last video
# --------------------------------------------------------------

last_video = openai.videos.list().data[0]
print("Model:", last_video.model)
print("Video status:", last_video.status)
print("Video progress:", last_video.progress)

# --------------------------------------------------------------
# Download the video
# --------------------------------------------------------------

video = download_sora_video(video=video, output_folder="./output")
