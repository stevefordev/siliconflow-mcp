import httpx
from .common import API_BASE_URL, API_KEY, IMAGE_DIR, ASPECT_RATIOS, download_file

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
