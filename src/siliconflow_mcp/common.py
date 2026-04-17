import os
import httpx
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_BASE_URL = "https://api.siliconflow.com/v1"
API_KEY = os.getenv("SILICONFLOW_API_KEY")
IMAGE_DIR = os.getenv("SILICONFLOW_IMAGE_DIR")
AUDIO_DIR = os.getenv("SILICONFLOW_AUDIO_DIR") or IMAGE_DIR

# Aspect Ratio to Image Size mapping
ASPECT_RATIOS = {
    "1:1": "1024x1024",
    "3:4": "768x1024",
    "4:3": "1024x768",
    "9:16": "576x1024",
    "16:9": "1024x576"
}

# Image Size for Video
VIDEO_SIZES = {
    "16:9": "1280x720",
    "9:16": "720x1280",
    "1:1": "960x960"
}

async def download_file(url: str, save_dir: str, prefix: str = "gen") -> str:
    """Download file from URL and save to local directory."""
    try:
        path = Path(save_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        # Determine extension
        ext = ".png"
        if ".mp4" in url.lower():
            ext = ".mp4"
        elif ".jpg" in url.lower() or ".jpeg" in url.lower():
            ext = ".jpg"
            
        filename = f"{prefix}_{int(time.time())}_{os.path.basename(url).split('?')[0]}"
        if not any(filename.endswith(s) for s in ['.png', '.jpg', '.jpeg', '.mp4']):
            filename += ext
            
        file_path = path / filename
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return str(file_path.absolute())
    except Exception as e:
        print(f"Failed to download file: {e}")
    return url

async def save_binary_file(content: bytes, save_dir: str, extension: str = "mp3", prefix: str = "audio") -> str:
    """Save binary content to local directory."""
    try:
        path = Path(save_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        filename = f"{prefix}_{int(time.time())}.{extension}"
        file_path = path / filename
        
        with open(file_path, "wb") as f:
            f.write(content)
        return str(file_path.absolute())
    except Exception as e:
        print(f"Failed to save binary file: {e}")
        return "Error saving file"
