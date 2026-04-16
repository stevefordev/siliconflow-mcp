import httpx
from .common import API_BASE_URL, API_KEY

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
