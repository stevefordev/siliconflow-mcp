import httpx
from .common import API_BASE_URL, API_KEY, AUDIO_DIR, save_binary_file

async def generate_speech(
    text: str,
    model: str = "fishaudio/fish-speech-1.5",
    voice: str = "fishaudio/fish-speech-1.5:alex",
    response_format: str = "mp3",
    sample_rate: int = 32000,
    speed: float = 1.0,
    gain: float = 0.0
) -> str:
    """
    Generate speech from text using SiliconFlow's API.
    
    Args:
        text: The text to generate speech for.
        model: The model to use for speech generation. 
               Options: "fishaudio/fish-speech-1.5", "IndexTeam/IndexTTS-2", "FunAudioLLM/CosyVoice2-0.5B"
        voice: The voice ID to use. 
               For fish-speech-1.5: "alex", "anna", "bella", "benjamin", "charles", "claire", "david", "diana"
               (Prefix with "fishaudio/fish-speech-1.5:" if not already)
        response_format: The format of the audio response. Options: "mp3", "opus", "wav", "pcm"
        sample_rate: The sample rate of the audio.
        speed: The speed of the speech (default 1.0).
        gain: The gain of the audio (default 0.0).
    """
    if not API_KEY:
        return "Error: SILICONFLOW_API_KEY environment variable is not set."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Ensure voice has the model prefix if it's a simple name and model is fish-speech
    if model == "fishaudio/fish-speech-1.5" and ":" not in voice:
        voice = f"{model}:{voice}"

    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
        "sample_rate": sample_rate,
        "speed": speed,
        "gain": gain
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/audio/speech",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                return f"Error: {response.status_code} - {response.text}"
            
            # The API returns binary audio data
            audio_content = response.content
            
            if AUDIO_DIR:
                local_path = await save_binary_file(
                    audio_content, 
                    AUDIO_DIR, 
                    extension=response_format, 
                    prefix="audio"
                )
                return f"Successfully generated speech!\nLocal Path: {local_path}"
            else:
                return "Successfully generated speech! (No local directory configured to save the file)"
                
    except Exception as e:
        return f"Exception: {str(e)}"
