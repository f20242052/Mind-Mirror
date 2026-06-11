"""
ai.py — Multi-provider AI backend for MindMirror.

Supported providers:
  - Ollama        (local, no key needed)
  - Groq          (cloud, BYOK)
  - OpenAI        (cloud, BYOK)
  - Custom        (any OpenAI-compatible endpoint, BYOK)
"""

import requests

# ── Provider constants ────────────────────────────────────────────────────────
PROVIDER_OLLAMA = "Ollama (Local)"
PROVIDER_GROQ = "Groq"
PROVIDER_OPENAI = "OpenAI"
PROVIDER_CUSTOM = "Custom (OpenAI-compatible)"

ALL_PROVIDERS = [PROVIDER_OLLAMA, PROVIDER_GROQ, PROVIDER_OPENAI, PROVIDER_CUSTOM]

# Default models per provider
DEFAULT_MODELS = {
    PROVIDER_OLLAMA: "llama3",
    PROVIDER_GROQ: "llama-3.3-70b-versatile",
    PROVIDER_OPENAI: "gpt-4o-mini",
    PROVIDER_CUSTOM: "your-model-name",
}

# Default base URLs
DEFAULT_URLS = {
    PROVIDER_OLLAMA: "http://localhost:11434",
    PROVIDER_GROQ: "https://api.groq.com/openai/v1",
    PROVIDER_OPENAI: "https://api.openai.com/v1",
    PROVIDER_CUSTOM: "http://localhost:1234/v1",
}


# ── Core chat function ────────────────────────────────────────────────────────
def _chat(
    system: str,
    user: str,
    max_tokens: int = 512,
    provider: str = PROVIDER_OLLAMA,
    model: str = None,
    api_key: str = None,
    base_url: str = None,
) -> str:
    """
    Send a chat request to the selected provider.
    Works with Ollama, Groq, OpenAI, or any OpenAI-compatible API.
    """
    model = model or DEFAULT_MODELS.get(provider, "llama3")
    base_url = base_url or DEFAULT_URLS.get(provider, "http://localhost:11434")

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    if provider == PROVIDER_OLLAMA:
        return _chat_ollama(base_url, model, messages, max_tokens)
    else:
        return _chat_openai_compatible(base_url, model, messages, max_tokens, api_key)


def _chat_ollama(base_url: str, model: str, messages: list, max_tokens: int) -> str:
    """Call Ollama's native API."""
    url = f"{base_url.rstrip('/')}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_predict": max_tokens},
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def _chat_openai_compatible(
    base_url: str, model: str, messages: list, max_tokens: int, api_key: str
) -> str:
    """Call any OpenAI-compatible API (Groq, OpenAI, Mistral, LM Studio, etc.)"""
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or ''}",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


# ── Provider config helper ────────────────────────────────────────────────────
def get_provider_config(session_state: dict) -> dict:
    """Extract provider config from Streamlit session_state."""
    return {
        "provider": session_state.get("ai_provider", PROVIDER_OLLAMA),
        "model": session_state.get("ai_model") or DEFAULT_MODELS.get(
            session_state.get("ai_provider", PROVIDER_OLLAMA), "llama3"
        ),
        "api_key": session_state.get("ai_api_key", ""),
        "base_url": session_state.get("ai_base_url") or DEFAULT_URLS.get(
            session_state.get("ai_provider", PROVIDER_OLLAMA), "http://localhost:11434"
        ),
    }


def check_ollama_connection(base_url: str = "http://localhost:11434") -> tuple[bool, str]:
    """Check if Ollama is running and return available models."""
    try:
        resp = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=5)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        return True, models
    except requests.exceptions.ConnectionError:
        return False, []
    except Exception as e:
        return False, []


# ── AI feature functions ──────────────────────────────────────────────────────
def generate_summary(title: str, content: str, mood: str, cfg: dict) -> str:
    system = (
        "You are a warm, empathetic journaling assistant. "
        "Summarize diary entries in 2-3 sentences, capturing the emotional essence "
        "and key moments. Be concise, personal, and compassionate."
    )
    user = f"Title: {title}\nMood: {mood}\n\nEntry:\n{content}"
    return _chat(system, user, max_tokens=200, **cfg)


def generate_reflection_prompt(title: str, content: str, mood: str, cfg: dict) -> str:
    system = (
        "You are a thoughtful journaling coach. Generate ONE meaningful, open-ended "
        "reflection question based on the diary entry. The question should encourage "
        "deeper self-exploration. Return only the question, nothing else."
    )
    user = f"Title: {title}\nMood: {mood}\n\nEntry:\n{content}"
    return _chat(system, user, max_tokens=100, **cfg)


def extract_themes(content: str, cfg: dict) -> list:
    system = (
        "You are an insightful journaling assistant. Extract 3-5 single-word or short "
        "two-word themes from a diary entry (e.g., 'family', 'work stress', 'gratitude'). "
        "Return ONLY a comma-separated list of themes, nothing else."
    )
    result = _chat(system, f"Entry:\n{content}", max_tokens=60, **cfg)
    themes = [t.strip() for t in result.split(",") if t.strip()]
    return themes[:5]


def generate_all_insights(title: str, content: str, mood: str, cfg: dict) -> dict:
    summary = generate_summary(title, content, mood, cfg)
    reflection = generate_reflection_prompt(title, content, mood, cfg)
    themes = extract_themes(content, cfg)
    return {
        "ai_summary": summary,
        "reflection_prompt": reflection,
        "themes": themes,
    }


def translate_text(text: str, language: str, cfg: dict) -> str:
    """Translate UI text to target language."""
    if language == "English":
        return text
    system = (
        f"You are a translator. Translate the given text to {language}. "
        "Return ONLY the translated text, nothing else. "
        "Keep emojis, punctuation marks, and special characters exactly as they are. "
        "Do not add any explanation or extra words."
    )
    return _chat(system, text, max_tokens=300, **cfg)
