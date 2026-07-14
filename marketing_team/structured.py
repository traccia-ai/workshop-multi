"""Run agents and parse JSON output — works reliably with Groq."""

from __future__ import annotations

import json
import re
from typing import TypeVar

from agents import Agent, Runner
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


def extract_json(text: str) -> str:
    """Pull a JSON object out of model text (handles markdown fences)."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text, flags=re.DOTALL)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        return text[start : end + 1]
    return text


async def run_structured(
    agent: Agent,
    prompt: str,
    model: type[T],
    *,
    retries: int = 3,
) -> T:
    """Call an agent and validate its response against a Pydantic model."""
    last_error: Exception | None = None
    current_prompt = prompt

    for attempt in range(retries):
        result = await Runner.run(agent, current_prompt)
        raw = str(result.final_output)
        try:
            return model.model_validate_json(extract_json(raw))
        except (ValidationError, json.JSONDecodeError, ValueError) as exc:
            last_error = exc
            current_prompt = (
                f"{prompt}\n\n"
                "Your last answer was not valid JSON. "
                f"Error: {exc}. "
                "Reply with ONLY a raw JSON object. No markdown, no commentary."
            )

    raise RuntimeError(
        f"Could not parse {model.__name__} after {retries} attempts: {last_error}"
    )
