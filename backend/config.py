import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

MOODS = [
    "😄 Happy",
    "😌 Calm",
    "😔 Sad",
    "😤 Frustrated",
    "😰 Anxious",
    "🥰 Grateful",
    "😴 Tired",
    "🔥 Motivated",
]

MOOD_COLORS = {
    "😄 Happy": "#FFD166",
    "😌 Calm": "#A8DADC",
    "😔 Sad": "#8BACD9",
    "😤 Frustrated": "#E07A5F",
    "😰 Anxious": "#C9B1D9",
    "🥰 Grateful": "#F4A5C0",
    "😴 Tired": "#B5B5B5",
    "🔥 Motivated": "#F4845F",
}
