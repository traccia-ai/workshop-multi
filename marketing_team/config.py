"""Shared model + env setup for the Marketing Agent Team workshop."""

from __future__ import annotations

import os
from functools import lru_cache

from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from dotenv import load_dotenv

load_dotenv()

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEFAULT_MODEL = "gemini-2.0-flash"


def get_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    if not key or key.startswith("your_"):
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Copy .env.example to .env and paste your "
            "free key from https://aistudio.google.com/apikey"
        )
    return key


def get_model_name() -> str:
    return os.getenv("MODEL_NAME", DEFAULT_MODEL)


@lru_cache(maxsize=1)
def get_model() -> OpenAIChatCompletionsModel:
    """Gemini via OpenAI-compatible Chat Completions (same pattern as Courses 1–2)."""
    client = AsyncOpenAI(api_key=get_api_key(), base_url=GEMINI_BASE_URL)
    # Prefer Traccia over OpenAI's built-in trace backend when using Gemini.
    set_default_openai_client(client=client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(disabled=True)
    return OpenAIChatCompletionsModel(model=get_model_name(), openai_client=client)


def init_observability(*, console: bool = True) -> None:
    """Initialize Traccia once. Safe to call from chapter scripts and Streamlit.

    Prefers project `traccia.toml`. Console exporter is enabled for local demos
    so participants see spans without a cloud key.
    """
    try:
        from traccia import init as traccia_init
    except ImportError:
        print("traccia not installed — run: pip install traccia")
        return

    try:
        traccia_init(openai_agents=True, enable_console_exporter=console)
    except TypeError:
        # Older / alternate kwargs — toml + bare init still works.
        traccia_init()
