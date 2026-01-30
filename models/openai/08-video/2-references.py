import time
from openai import OpenAI
from pathlib import Path
import base64
from utils.resizer import resize_image
from utils.downloader import download_sora_video

openai = OpenAI()


# --------------------------------------------------------------
# Generate a reference image
# --------------------------------------------------------------

# Takes abbout 2 minutes
response = openai.responses.create(
    model="gpt-5",
    input="A professional studio desk setup with Shure SM7B microphone on boom arm. Dark background with soft blue LED light glow creating ambient atmosphere. Clean desk surface, professional lighting equipment visible. Cinematic look, moody lighting, no people.",
    tools=[
        {
            "type": "image_generation",
            "size": "1024x1536",
            "quality": "high",
        }
    ],
)


# --------------------------------------------------------------
# Resize the image to 720x1280 and save it
# --------------------------------------------------------------

message_outputs = [output for output in response.output if output.type == "message"]

if message_outputs:
    for msg in message_outputs:
        for content in msg.content:
            if hasattr(content, "text"):
                print(f"API Response: {content.text}")

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    image_path = f"./references/{response.id}.png"
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_base64))
    resize_image(image_path)
    print(f"Saved and resized image to 720x1280: {image_path}")
else:
    print("No image was generated. Check the API response above.")

# --------------------------------------------------------------
# Use input reference image
# --------------------------------------------------------------

# The moderation here is quite strict.
# You might need to try different images/prompts if you get an error.

video = openai.videos.create(
    model="sora-2",
    prompt="Make this image come to life",
    input_reference=Path(f"./references/{response.id}.png"),
    size="720x1280",
    seconds=4,
)

print("Video generation started:", video)


# --------------------------------------------------------------
# Get last video
# --------------------------------------------------------------

time.sleep(3)
last_video = openai.videos.list().data[0]

# --------------------------------------------------------------
# Download the video
# --------------------------------------------------------------

video = download_sora_video(video=last_video, output_folder="./output")
