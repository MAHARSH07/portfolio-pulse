import httpx

from app.ai.providers.base import LLMProvider
from app.core.config import settings


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model: str,
        base_url: str,
    ):
        self.model = model
        self.base_url = base_url
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]
