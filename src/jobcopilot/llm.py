import json
from dataclasses import dataclass

import httpx


@dataclass
class LlmResponse:
    content: str
    model: str
    input_tokens: int
    output_tokens: int


class LlmError(Exception):
    pass


class LlmClient:
    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def complete(self, system: str, user: str) -> LlmResponse:
        if not self.api_key:
            raise LlmError("LLM_API_KEY is not set")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
        if response.status_code != 200:
            raise LlmError(f"LLM request failed: {response.status_code} {response.text[:200]}")
        data = response.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})
        return LlmResponse(
            content=choice["message"]["content"],
            model=data.get("model", self.model),
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
        )


def extract_json(content: str) -> dict:
    text = content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)
