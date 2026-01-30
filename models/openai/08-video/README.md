# Sora 2 API - Video Generation Tutorial

Learn how to generate videos with OpenAI's Sora 2 API using Python. This tutorial walks you through text-to-video generation, image animation, remixing, and creating multi-shot sequences.

## What We'll Build

In this tutorial, you'll learn to:

1. **Basic Video Generation** (`1-sora-quickstart.py`) - Generate a 4-second video from a text prompt
2. **Image-to-Video** (`2-references.py`) - Create a reference image with GPT-5 and animate it with Sora
3. **Pro Model** (`3-sora-pro-mode.py`) - Use the higher-quality `sora-2-pro` model (currently experiencing delays)
4. **AI-Enhanced Prompting** (`4-sora-prompting.py`) - Let GPT-5 improve your video prompts
5. **Remix Videos** (`5-sora-remix.py`) - Generate variations of existing videos while maintaining consistency
6. **Multi-Shot Sequences** (`6-sora-sequence.py`) - Stitch multiple videos together using FFmpeg

## Prerequisites

- Python 3.10+
- [OpenAI API key](https://platform.openai.com/api-keys) with Sora access
- FFmpeg installed on your system

## Installation

```bash
# Install Python dependencies
pip install openai pydantic requests pillow

# Install FFmpeg (macOS)
brew install ffmpeg

# Install FFmpeg (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Install FFmpeg (Windows)
# Download from: https://ffmpeg.org/download.html
```

## Important Notes

⚠️ **Content Moderation**: Sora has heavy moderation, especially for:
- Videos depicting real people (image-to-video with people is not supported)
- Certain subject matter or scenarios

⚠️ **Pricing**: Sora API usage can be expensive. Monitor your usage at [OpenAI's usage dashboard](https://platform.openai.com/usage).

⚠️ **Pro Model Status**: The `sora-2-pro` model currently gets stuck in progress during generation. Use `sora-2` for reliable results.

⚠️ **Cameo Feature**: The cameo option is not yet available via the API.

## Official Documentation

- [Video Generation Guide](https://platform.openai.com/docs/guides/video-generation)
- [Sora 2 Pro Model](https://platform.openai.com/docs/models/sora-2-pro)
- [Sora 2 Model](https://platform.openai.com/docs/models/sora-2)
- [Sora Prompting Guide](https://cookbook.openai.com/examples/sora/sora2_prompting_guide)

