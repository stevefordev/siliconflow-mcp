import os
import httpx
import json
import base64
import time
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("siliconflow-mcp")

# Constants
API_BASE_URL = "https://api.siliconflow.com/v1"
API_KEY = os.getenv("SILICONFLOW_API_KEY")
IMAGE_DIR = os.getenv("SILICONFLOW_IMAGE_DIR")

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

@mcp.tool()
async def generate_image(
    prompt: str,
    model: str = "black-forest-labs/FLUX.1-schnell",
    aspect_ratio: str = "1:1",
    image_size: str = None,
    num_images: int = 1,
    seed: int = None,
    negative_prompt: str = None,
    output_format: str = "png"
) -> str:
    """
    Generate interactive images using SiliconFlow's API.
    """
    if not API_KEY:
        return "Error: SILICONFLOW_API_KEY environment variable is not set."

    res = image_size
    if aspect_ratio in ASPECT_RATIOS:
        res = ASPECT_RATIOS[aspect_ratio]
    elif not res:
        res = "1024x1024"

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "image_size": res,
        "output_format": output_format,
        "batch_size": min(max(num_images, 1), 4)
    }
    if seed is not None: payload["seed"] = seed
    if negative_prompt: payload["negative_prompt"] = negative_prompt

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{API_BASE_URL}/images/generations", headers=headers, json=payload)
            if response.status_code != 200: return f"Error: {response.status_code} - {response.text}"
            data = response.json()
            images = data.get("images", [])
            if not images: return "Error: No images were generated."
            
            result_text = f"Successfully generated {len(images)} image(s):\n"
            for i, img in enumerate(images):
                url = img.get("url")
                if IMAGE_DIR:
                    local_path = await download_file(url, IMAGE_DIR, "img")
                    result_text += f"{i+1}. Local Path: {local_path}\n   URL: {url}\n"
                else:
                    result_text += f"{i+1}. URL: {url}\n"
            return result_text
    except Exception as e:
        return f"Exception: {str(e)}"

@mcp.tool()
async def edit_image(
    image: str,
    prompt: str,
    model: str = "Qwen/Qwen-Image-Edit-2509"
) -> str:
    """Edit an existing image using SiliconFlow's API."""
    if not API_KEY: return "Error: SILICONFLOW_API_KEY environment variable is not set."
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "image": image}
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{API_BASE_URL}/images/generations", headers=headers, json=payload)
            if response.status_code != 200: return f"Error: {response.status_code} - {response.text}"
            data = response.json()
            images = data.get("images", [])
            if not images: return "Error: No images were generated."
            url = images[0].get("url")
            if IMAGE_DIR:
                local_path = await download_file(url, IMAGE_DIR, "edit")
                return f"Successfully edited image!\nLocal Path: {local_path}\nURL: {url}"
            return f"Successfully edited image!\nURL: {url}"
    except Exception as e:
        return f"Exception: {str(e)}"

@mcp.tool()
async def submit_video_generation(
    prompt: str,
    model: str = "Wan-AI/Wan2.2-T2V-A14B",
    aspect_ratio: str = "16:9",
    negative_prompt: str = None,
    seed: int = None
) -> str:
    """Submit a video generation request to SiliconFlow."""
    if not API_KEY: return "Error: SILICONFLOW_API_KEY environment variable is not set."
    
    size = VIDEO_SIZES.get(aspect_ratio, "1280x720")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "image_size": size}
    if negative_prompt: payload["negative_prompt"] = negative_prompt
    if seed is not None: payload["seed"] = seed

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{API_BASE_URL}/video/submit", headers=headers, json=payload)
            if response.status_code != 200: return f"Error: {response.status_code} - {response.text}"
            return response.json().get("requestId", "Error: No requestId returned")
    except Exception as e:
        return f"Exception: {str(e)}"

@mcp.tool()
async def get_video_status(request_id: str) -> str:
    """Check the status of a video generation request."""
    if not API_KEY: return "Error: SILICONFLOW_API_KEY environment variable is not set."
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"requestId": request_id}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{API_BASE_URL}/video/status", headers=headers, json=payload)
            if response.status_code != 200: return f"Error: {response.status_code} - {response.text}"
            data = response.json()
            status = data.get("status")
            if status == "Succeed":
                video_url = data.get("results", {}).get("videos", [{}])[0].get("url")
                return f"STATUS: Succeed\nURL: {video_url}"
            return f"STATUS: {status}\nREASON: {data.get('reason', 'N/A')}"
    except Exception as e:
        return f"Exception: {str(e)}"

@mcp.tool()
async def generate_video(
    prompt: str,
    model: str = "Wan-AI/Wan2.2-T2V-A14B",
    aspect_ratio: str = "16:9",
    polling_interval: int = 15,
    max_wait_seconds: int = 300
) -> str:
    """Generate a video and wait for it to complete (auto-polling)."""
    request_id = await submit_video_generation(prompt=prompt, model=model, aspect_ratio=aspect_ratio)
    if request_id.startswith("Error") or request_id.startswith("Exception"): return request_id
    
    start_time = time.time()
    while time.time() - start_time < max_wait_seconds:
        status_result = await get_video_status(request_id)
        if "STATUS: Succeed" in status_result:
            url = status_result.split("URL: ")[1].strip()
            if IMAGE_DIR:
                local_path = await download_file(url, IMAGE_DIR, "video")
                return f"Successfully generated video!\nLocal Path: {local_path}\nURL: {url}"
            return f"Successfully generated video!\nURL: {url}"
        elif "STATUS: Failed" in status_result:
            return f"Video generation failed: {status_result}"
        
        await asyncio.sleep(polling_interval)
        
    return f"Timeout: Video generation is still in progress (Request ID: {request_id})"

@mcp.tool()
async def get_user_info() -> str:
    """
    Get user account information, including credit balance and basic profile.
    """
    if not API_KEY:
        return "Error: SILICONFLOW_API_KEY environment variable is not set."

    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/user/info", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("status"):
                    user_data = data.get("data", {})
                    user_id = user_data.get("id", "N/A")
                    name = user_data.get("name", "N/A")
                    email = user_data.get("email", "N/A")
                    balance = user_data.get("balance", "N/A")
                    charge_balance = user_data.get("chargeBalance", "N/A")
                    total_balance = user_data.get("totalBalance", "N/A")
                    status = user_data.get("status", "N/A")
                    
                    result = (
                        f"User Info:\n"
                        f"- ID: {user_id}\n"
                        f"- Name: {name}\n"
                        f"- Email: {email}\n"
                        f"- Total Balance: $ {total_balance}\n"
                        f"- Charge Balance (Paid): $ {charge_balance}\n"
                        f"- Free Balance: $ {balance}\n"
                        f"- Account Status: {status}"
                    )
                    return result
                return f"Error: API returned status false. Message: {data.get('message')}"
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

@mcp.tool()
async def list_models() -> str:
    """List available image and video models from SiliconFlow."""
    if not API_KEY: return "Error: SILICONFLOW_API_KEY environment variable is not set."
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/models", headers=headers)
            if response.status_code == 200:
                data = response.json()
                models = [m.get("id") for m in data.get("data", [])]
                img_video_models = [m for m in models if any(x in m.lower() for x in ["flux", "stable-diffusion", "qwen-image", "kolors", "wan", "i2v", "t2v"])]
                return "Available Models:\n" + "\n".join(img_video_models)
            return "Failed to fetch model list."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
