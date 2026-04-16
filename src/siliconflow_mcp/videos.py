import httpx
import time
import asyncio
from .common import API_BASE_URL, API_KEY, IMAGE_DIR, VIDEO_SIZES, download_file

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
