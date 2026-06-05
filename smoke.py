from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import requests
from anthropic import Anthropic
from openai import OpenAI
from together import Together

from modest_proposal.config import Settings, normalize_ollama_host

ProviderName = Literal["ollama", "openai", "anthropic", "together"]


@dataclass(frozen=True)
class SmokeRequest:
    provider: ProviderName
    model: str
    prompt: str
    temperature: float | None = None
    max_tokens: int | None = None
    reasoning_effort: str | None = None
    reasoning_enabled: bool | None = None
    anthropic_effort: str | None = None
    anthropic_thinking: bool = False
    timeout_s: float | None = None


def run_smoke_test(request: SmokeRequest, settings: Settings | None = None) -> str:
    config = settings or Settings()

    if request.provider == "ollama":
        return _run_ollama(request, config)
    if request.provider == "openai":
        return _run_openai(request, config)
    if request.provider == "anthropic":
        return _run_anthropic(request, config)
    if request.provider == "together":
        return _run_together(request, config)

    raise ValueError(f"Unsupported provider: {request.provider}")


def _run_ollama(request: SmokeRequest, settings: Settings) -> str:
    payload = {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False,
        "options": {},
    }
    if request.temperature is not None:
        payload["options"]["temperature"] = request.temperature
    if request.max_tokens is not None:
        payload["options"]["num_predict"] = request.max_tokens
    response = requests.post(
        f"{normalize_ollama_host(settings.ollama_host)}/api/chat",
        json=payload,
        timeout=request.timeout_s or 120,
    )
    response.raise_for_status()
    data = response.json()
    content = data.get("message", {}).get("content", "").strip()
    if not content:
        raise RuntimeError(f"Ollama returned an unexpected payload: {data}")
    return content


def _run_openai(request: SmokeRequest, settings: Settings) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=settings.openai_api_key)
    payload: dict[str, object]
    last_response: object | None = None

    for _ in range(3):
        payload = {
            "model": request.model,
            "input": request.prompt,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_tokens is not None:
            payload["max_output_tokens"] = request.max_tokens
        if request.reasoning_effort:
            payload["reasoning"] = {"effort": request.reasoning_effort}

        response = client.responses.create(**payload, timeout=request.timeout_s)
        last_response = response
        content = response.output_text
        if content and content.strip():
            return content.strip()

    raise RuntimeError(f"OpenAI returned an empty response: {last_response.model_dump()}")


def _run_anthropic(request: SmokeRequest, settings: Settings) -> str:
    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    client = Anthropic(api_key=settings.anthropic_api_key)
    payload: dict[str, object] = {
        "model": request.model,
        "max_tokens": request.max_tokens or (2048 if request.anthropic_thinking else 100),
        "messages": [{"role": "user", "content": request.prompt}],
    }
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    if request.anthropic_effort:
        payload["output_config"] = {"effort": request.anthropic_effort}
    if request.anthropic_thinking:
        payload["thinking"] = {"type": "adaptive"}

    response = client.messages.create(**payload, timeout=request.timeout_s)
    parts = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    content = "\n".join(part.strip() for part in parts if part.strip())
    if not content:
        raise RuntimeError("Anthropic returned an empty response.")
    return content


def _run_together(request: SmokeRequest, settings: Settings) -> str:
    if not settings.together_api_key:
        raise RuntimeError("TOGETHER_API_KEY is not set.")

    client = Together(api_key=settings.together_api_key)
    payload: dict[str, object] = {
        "model": request.model,
        "messages": [{"role": "user", "content": request.prompt}],
    }
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    if request.max_tokens is not None:
        payload["max_tokens"] = request.max_tokens
    if request.reasoning_effort:
        payload["reasoning_effort"] = request.reasoning_effort
    if request.reasoning_enabled is not None:
        payload["reasoning"] = {"enabled": request.reasoning_enabled}

    response = client.chat.completions.create(**payload, timeout=request.timeout_s)
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError(f"Together returned an empty response: {response.model_dump()}")
    return content.strip()
