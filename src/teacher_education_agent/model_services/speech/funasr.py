"""OpenAI-compatible FunASR/SenseVoice client."""
from pathlib import Path
from teacher_education_agent.core.config import Settings
class FunASRClient:
    def __init__(self, settings: Settings): self.settings = settings
    async def transcribe(self, path: Path) -> dict:
        if not path.is_file(): raise ValueError("audio file does not exist")
        import httpx
        async with httpx.AsyncClient(timeout=600) as client:
            with path.open("rb") as audio:
                response = await client.post(f"{self.settings.funasr_base_url.rstrip('/')}/v1/audio/transcriptions", files={"file": (path.name, audio)}, data={"model": self.settings.funasr_model})
        response.raise_for_status()
        return response.json()
