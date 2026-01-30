from utils.director import SoraDirector
from utils.downloader import download_sora_video
from openai import OpenAI

openai = OpenAI()
director = SoraDirector()
# --------------------------------------------------------------
# Generate a Sora prompt
# --------------------------------------------------------------

prompt = director.generate_sora_prompt(
    "A YouTuber excitedly showing OpenAI's new Sora 2 API release to generate hyper-realistic videos with just a few lines of code."
)
print(prompt)


# --------------------------------------------------------------
# Generate a video
# --------------------------------------------------------------

video = openai.videos.create(
    model="sora-2",
    prompt=prompt,
    size="720x1280",
    seconds="4",
)

print("Video generation started:", video)

# --------------------------------------------------------------
# Download the video
# --------------------------------------------------------------

video = download_sora_video(video=video, output_folder="./output")
