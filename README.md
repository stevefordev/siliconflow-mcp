# SiliconFlow MCP Server

[[English](README.md) | [한국어](README.ko.md)]

An MCP (Model Context Protocol) server for SiliconFlow's image generation service. This allows AI models (like Claude) to generate high-quality images directly using various models available on SiliconFlow.

## Features

- **`generate_image` tool**: Generate images from text prompts.
  - Supports multiple models (FLUX.1-schnell, FLUX.1-dev, FLUX.2-pro, etc.)
  - **`aspect_ratio` support**: Choose from 1:1, 16:9, 9:16, etc.
  - Supports `negative_prompt` for supported models.
  - Customizable seeds for reproducible generations.
- **`generate_video` tool**: Generate videos via text prompts (auto-polls until completion).
  - Supports Wan-AI models and customizable aspect ratios.
- **`submit_video_generation` & `get_video_status`**: Low-level tools for manual async video management.
- **`list_models` tool**: Dynamically fetch available image and video models.
- **`get_user_info` tool**: Check your SiliconFlow account details, including balance (Total, Paid, Free) and profile info.
- **Local Saving**: Automatically save `.png`, `.jpg`, or `.mp4` files to your specified directory.

## Setup

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) installed (recommended).
- A SiliconFlow API Key. Get one at [SiliconFlow Dashboard](https://cloud.siliconflow.com/account/ak).

### 2. Configuration
Create a `.env` file in the project root (you can copy from `.env.example`):
```bash
SILICONFLOW_API_KEY=your_api_key_here
# Optional: Path to save generated images locally
SILICONFLOW_IMAGE_DIR=C:/path/to/save/images
```

### 3. Usage with MCP Clients

This server can be used with any MCP-compatible client.

#### Claude Desktop
Add the following to your Claude Desktop configuration file (`%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/path/to/siliconflow-mcp",
        "run",
        "siliconflow_mcp"
      ]
    }
  }
}
```

#### Claude Code
Run the following command to add the server:
```bash
claude mcp add siliconflow -- uv --directory C:/path/to/siliconflow-mcp run siliconflow_mcp
```

#### Gemini CLI
Add the configuration to your `settings.json` (usually located in `.gemini/settings.json`):
```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/path/to/siliconflow-mcp",
        "run",
        "siliconflow_mcp"
      ]
    }
  }
}
```

#### GPT Codex
Configure the MCP server in your GPT Codex settings following the standard MCP server format:
- **Name**: `siliconflow`
- **Command**: `uv`
- **Args**: `["--directory", "C:/path/to/siliconflow-mcp", "run", "siliconflow_mcp"]`

*Note: Always replace `C:/path/to/siliconflow-mcp` with the actual absolute path to this directory.*

## Installation for Developers

```bash
# Install dependencies
uv sync

# Run the server locally
uv run siliconflow_mcp
```

## Supported Models
- `black-forest-labs/FLUX.1-schnell` (Fast and efficient)
- `black-forest-labs/FLUX.1-dev` (Higher quality)
- `black-forest-labs/FLUX.2-pro` (Professional grade)
- ...and other image models hosted on SiliconFlow.

## License
MIT
