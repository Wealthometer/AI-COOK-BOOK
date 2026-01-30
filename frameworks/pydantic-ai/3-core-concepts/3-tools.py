import json

import nest_asyncio
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from youtube_transcript_api import YouTubeTranscriptApi

from utils.youtube import extract_video_id

nest_asyncio.apply()


class Transcript(BaseModel):
    video_id: str
    language: str
    text: str
    word_count: int


# --------------------------------------------------------------
# Basic tool - get YouTube transcript with structured output
# --------------------------------------------------------------

agent = Agent("openai:gpt-4o-mini", instructions="You are a helpful YouTube assistant.")


@agent.tool_plain
def get_transcript(video_url_or_id: str) -> Transcript:
    """
    Get the transcript for a YouTube video using either the video URL or video ID.
    Returns a structured Transcript object with video info and text.

    https://github.com/jdepoix/youtube-transcript-api
    """
    try:
        video_id = extract_video_id(video_url_or_id)
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        text = " ".join([snippet.text for snippet in transcript])

        return Transcript(
            video_id=video_id,
            language=transcript.language,
            text=text,
            word_count=len(text.split()),
        )
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {str(e)}")


result = agent.run_sync(
    "What is this video about? https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)
print(result.output)

# --------------------------------------------------------------
# Let's explore the result
# --------------------------------------------------------------

messages = json.loads(result.all_messages_json())
print(json.dumps(messages, indent=2))

# --------------------------------------------------------------
# Tool with dependencies - personalized transcript language
# --------------------------------------------------------------


class UserPreferences(BaseModel):
    name: str
    preferred_language: str


user_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=UserPreferences,
    instructions="You are a helpful YouTube assistant.",
)


@user_agent.tool
def get_user_transcript(ctx: RunContext[UserPreferences], video_url: str) -> Transcript:
    """
    Get the transcript for a YouTube video in the user's preferred language.
    Returns a structured Transcript object.
    """
    try:
        video_id = extract_video_id(video_url)
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=[ctx.deps.preferred_language])
        text = " ".join([snippet.text for snippet in transcript])

        return Transcript(
            video_id=video_id,
            language=transcript.language,
            text=text,
            word_count=len(text.split()),
        )
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {str(e)}")


@user_agent.instructions
def add_user_context(ctx: RunContext[UserPreferences]) -> str:
    return f"User: {ctx.deps.name}, Preferred language: {ctx.deps.preferred_language}"


user_prefs = UserPreferences(name="Alice", preferred_language="es")
result = user_agent.run_sync(
    "What is this video about? https://www.youtube.com/watch?v=4JDu69Jy41Y",
    deps=user_prefs,
)
print(result.output)


messages = json.loads(result.all_messages_json())
print(json.dumps(messages, indent=2))

# --------------------------------------------------------------
# Multi-turn tool calls - agent orchestrates multiple tools
# --------------------------------------------------------------

multi_agent = Agent(
    "openai:gpt-4o",  # Use a more powerful model for multi-turn tool calls
    instructions="You are a video content analyzer. Use tools to analyze videos.",
)


@multi_agent.tool_plain
def fetch_transcript(video_url: str) -> Transcript:
    """Fetch the transcript of a YouTube video."""
    video_id = extract_video_id(video_url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    text = " ".join([snippet.text for snippet in transcript])

    return Transcript(
        video_id=video_id,
        language=transcript.language,
        text=text,
        word_count=len(text.split()),
    )


@multi_agent.tool_plain
def count_keyword(text: str, keyword: str) -> int:
    """Count how many times a keyword appears in text (case-insensitive)."""
    return text.lower().count(keyword.lower())


result = multi_agent.run_sync(
    "Get the transcript for https://www.youtube.com/watch?v=dQw4w9WgXcQ and tell me how many times the word 'never' appears"
)
print("\n--- Multi-turn Result ---")
print(result.output)

print("\n--- Tool Calls Made ---")
messages = result.all_messages()
for msg in messages:
    if msg.kind == "response":
        for part in msg.parts:
            if part.part_kind == "tool-call":
                print(f"  • {part.tool_name}()")


# --------------------------------------------------------------
# Validation of tool calls
# --------------------------------------------------------------

transcript = fetch_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(transcript)

count = count_keyword(transcript.text, "never")
print(count)
assert count == 40
