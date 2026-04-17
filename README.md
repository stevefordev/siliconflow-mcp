# SiliconFlow MCP Server

[[English](README.md) | [한국어](README.ko.md)]

An MCP (Model Context Protocol) server for SiliconFlow's generative services. This allows AI models (like Claude) to generate high-quality images, videos, and speech directly using various models available on SiliconFlow.

- **Service**: [SiliconFlow](https://www.siliconflow.com/)
- **API Documentation**: [SiliconFlow API Reference](https://docs.siliconflow.com/en/api-reference)

## Features

- **`generate_image` tool**: Generate images from text prompts.
  - Supports multiple models (FLUX.1-schnell, FLUX.1-dev, FLUX.2-pro, etc.)
  - **`aspect_ratio` support**: Choose from 1:1, 16:9, 9:16, etc.
  - Supports `negative_prompt` for supported models.
  - Customizable seeds for reproducible generations.
- **`generate_video` tool**: Generate videos via text prompts (auto-polls until completion).
  - Supports Wan-AI models and customizable aspect ratios.
- **`generate_speech` tool**: Generate speech (TTS) from text.
  - Supports `fish-speech`, `IndexTTS`, and `CosyVoice` models.
  - Customizable voices, response formats (mp3, wav, etc.), and speed.
- **`submit_video_generation` & `get_video_status`**: Low-level tools for manual async video management.
- **`list_models` tool**: Dynamically fetch available image, video, and audio models.
- **`get_user_info` tool**: Check your SiliconFlow account details, including balance (Total, Paid, Free) and profile info.
- **Local Saving**: Automatically save `.png`, `.jpg`, `.mp4`, or `.mp3` files to your specified directory.

## Setup

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) installed (recommended) or Python 3.10+.
- A SiliconFlow API Key. Get one at [SiliconFlow Dashboard](https://cloud.siliconflow.com/account/ak).

### 2. Configuration
The server requires an API key to function. You can provide it via environment variables or a `.env` file.

```bash
SILICONFLOW_API_KEY=your_api_key_here
# Optional: Path to save generated images/videos locally
SILICONFLOW_IMAGE_DIR=/path/to/save/assets
# Optional: Path to save generated audio files (defaults to IMAGE_DIR)
SILICONFLOW_AUDIO_DIR=/path/to/save/audio
```

## Usage

### Using with uvx (Recommended)
You don't need to install anything locally. Just run it directly using `uvx`:

```bash
uvx siliconflow-mcp
```

### Installation via PyPI
You can also install it as a global tool:

```bash
uv tool install siliconflow-mcp
# or using pip
pip install siliconflow-mcp
```

### Configuration for MCP Clients

#### Claude Desktop
Add the following to your Claude Desktop configuration file (`%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uvx",
      "args": ["siliconflow-mcp"],
      "env": {
        "SILICONFLOW_API_KEY": "your_api_key_here",
        "SILICONFLOW_IMAGE_DIR": "/path/to/save/assets",
        "SILICONFLOW_AUDIO_DIR": "/path/to/save/audio"
      }
    }
  }
}
```

#### Claude Code
Run the following command:
```bash
claude mcp add siliconflow \
-e SILICONFLOW_API_KEY="your_api_key_here" \
-e SILICONFLOW_IMAGE_DIR="/path/to/save/assets" \
-e SILICONFLOW_AUDIO_DIR="/path/to/save/audio" \
-- uvx siliconflow-mcp
```

#### Gemini CLI
Run the following command:
```bash
gemini mcp add siliconflow \
-e SILICONFLOW_API_KEY="your_api_key_here" \
-e SILICONFLOW_IMAGE_DIR="/path/to/save/assets" \
-e SILICONFLOW_AUDIO_DIR="/path/to/save/audio" \
uvx siliconflow-mcp
```

Manual: Add the configuration to your `settings.json` (usually located in `.gemini/settings.json`):
```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uvx",
      "args": ["siliconflow-mcp"],
      "env": {
        "SILICONFLOW_API_KEY": "your_api_key_here",
        "SILICONFLOW_IMAGE_DIR": "/path/to/save/assets",
        "SILICONFLOW_AUDIO_DIR": "/path/to/save/audio"
      }
    }
  }
}
```

## Installation for Developers
If you want to contribute or run from source:

```bash
# Install dependencies
uv sync

# Run the server locally
uv run siliconflow_mcp
```

## Supported Models

### Image Models
- `black-forest-labs/FLUX.1-schnell` (Fast and efficient)
- `black-forest-labs/FLUX.1-dev` (High fidelity)
- `black-forest-labs/FLUX.1-pro` (Top-tier quality)
- `stabilityai/stable-diffusion-3-5-large`
- `stabilityai/stable-diffusion-3-5-large-turbo`
- `stabilityai/stable-diffusion-xl-base-1.0`
- `ByteDance/SDXL-Lightning`
- `Kwai-Kolors/Kolors`
- `Qwen/Qwen-Image-Edit-2509` (Image editing)

### Video Models
- `Wan-AI/Wan2.2-T2V-A14B` (Text-to-Video)
- `Wan-AI/Wan2.1-T2V-14B`
- `Wan-AI/Wan2.1-I2V-14B-720P` (Image-to-Video)
- `Wan-AI/Wan2.1-T2V-1.3B`

### Audio (TTS) Models
- `fishaudio/fish-speech-1.5`
- `IndexTeam/IndexTTS-2`
- `FunAudioLLM/CosyVoice2-0.5B`

You can use the `list_models` tool to see the full list of available models from SiliconFlow.

## License
MIT
