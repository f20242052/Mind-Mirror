from groq import Groq
from backend.config import GROQ_API_KEY, GROQ_MODEL

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def _chat(system: str, user: str, max_tokens: int = 512) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def generate_summary(title: str, content: str, mood: str) -> str:
    system = (
        "You are a warm, empathetic journaling assistant. "
        "Summarize diary entries in 2-3 sentences, capturing the emotional essence "
        "and key moments. Be concise, personal, and compassionate."
    )
    user = f"Title: {title}\nMood: {mood}\n\nEntry:\n{content}"
    return _chat(system, user, max_tokens=200)


def generate_reflection_prompt(title: str, content: str, mood: str) -> str:
    system = (
        "You are a thoughtful journaling coach. Generate ONE meaningful, open-ended "
        "reflection question based on the diary entry. The question should encourage "
        "deeper self-exploration. Return only the question, nothing else."
    )
    user = f"Title: {title}\nMood: {mood}\n\nEntry:\n{content}"
    return _chat(system, user, max_tokens=100)


def extract_themes(content: str) -> list[str]:
    system = (
        "You are an insightful journaling assistant. Extract 3-5 single-word or short "
        "two-word themes from a diary entry (e.g., 'family', 'work stress', 'gratitude'). "
        "Return ONLY a comma-separated list of themes, nothing else."
    )
    user = f"Entry:\n{content}"
    result = _chat(system, user, max_tokens=60)
    themes = [t.strip() for t in result.split(",") if t.strip()]
    return themes[:5]


def generate_all_insights(title: str, content: str, mood: str) -> dict:
    summary = generate_summary(title, content, mood)
    reflection = generate_reflection_prompt(title, content, mood)
    themes = extract_themes(content)
    return {
        "ai_summary": summary,
        "reflection_prompt": reflection,
        "themes": themes,
    }
