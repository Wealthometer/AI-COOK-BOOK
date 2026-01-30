import os
from datetime import datetime
from openai import OpenAI
from utils.downloader import download_sora_video

openai = OpenAI()

# Character description for consistency
CHARACTER = (
    "A 30-year-old male programmer with short dark hair, beard, wearing a black t-shirt"
)

shots = [
    # Shot 1: Kitchen Hook - The attention grabber
    f"{CHARACTER} standing in a modern kitchen, holding a coffee mug, looking directly at the camera with wide eyes and an excited expression. He says: 'OpenAI just dropped Sora 2 API at 2am... I've been up all night, this is INSANE.' Natural morning light from window, handheld camera feel, shot on Sony FX3, shallow depth of field, vertical 9:16 format. Kitchen counter and coffee machine visible in background.",
    # Shot 2: Walking/Hallway Transition - The value proposition
    "The same man walking through a hallway toward his office, maintaining his appearance from the previous shot. Gesturing animatedly while talking to the camera. He says with enthusiasm: 'Generate videos with 10 lines of Python. B-roll? Done. Product demos? Easy.' Tracking shot following him, natural indoor lighting transitioning to office glow, shot on Sony FX3 with gimbal, cinematic movement, vertical format.",
    # Shot 3: Office Desk Payoff - The promise
    "The same man now sitting at his professional studio desk with Shure SM7B microphone on boom arm. Same appearance and clothing. Dark background with soft blue LED light glow. He leans forward with a confident smile and says: 'In this video I'll show you how to use Sora 2 API and the prompting tricks that work. Let's go.' Professional three-point lighting, shot on Sony FX3, cinematic depth of field, vertical 9:16 format.",
]

# Create unique sequence folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"./output/sequence_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

print("Creating 3-shot sequence using remix...\n")
print(f"Output folder: {output_dir}\n")

# --------------------------------------------------------------
# Create Shot 1
# --------------------------------------------------------------

print("Generating Shot 1...")
video = openai.videos.create(
    model="sora-2",
    prompt=shots[0],
    size="720x1280",
    seconds="8",
)

print("Shot 1 generation started:", video)
video = download_sora_video(video, output_dir, "shot_1")

# --------------------------------------------------------------
# Remix to Shot 2
# --------------------------------------------------------------

print("\nGenerating Shot 2 via remix...")
remix_video = openai.videos.remix(
    video_id=video.id,
    prompt=shots[1],
)

print("Shot 2 generation started:", remix_video)
remix_video = download_sora_video(remix_video, output_dir, "shot_2")

# --------------------------------------------------------------
# Remix to Shot 3
# --------------------------------------------------------------

print("\nGenerating Shot 3 via remix...")
remix_video_2 = openai.videos.remix(
    video_id=video.id,
    prompt=shots[2],
)

print("Shot 3 generation started:", remix_video_2)
remix_video_2 = download_sora_video(remix_video_2, output_dir, "shot_3")

print(f"\n✓ All 3 shots saved to {output_dir}/")
print("\nUse 6-sora-sequence.py to stitch them together!")
