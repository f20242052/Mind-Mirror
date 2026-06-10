from supabase import create_client
from backend.config import SUPABASE_URL, SUPABASE_ANON_KEY


def _client(access_token: str):
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.postgrest.auth(access_token)
    return client


def create_entry(access_token: str, user_id: str, title: str, content: str, mood: str,
                 ai_summary: str = None, reflection_prompt: str = None, themes: list = None):
    client = _client(access_token)
    data = {
        "user_id": user_id,
        "title": title,
        "content": content,
        "mood": mood,
        "ai_summary": ai_summary,
        "reflection_prompt": reflection_prompt,
        "themes": themes or [],
    }
    response = client.table("diary_entries").insert(data).execute()
    return response.data[0] if response.data else None


def get_entries(access_token: str, user_id: str):
    client = _client(access_token)
    response = (
        client.table("diary_entries")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def get_entry(access_token: str, entry_id: str, user_id: str):
    client = _client(access_token)
    response = (
        client.table("diary_entries")
        .select("*")
        .eq("id", entry_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    return response.data


def update_entry(access_token: str, entry_id: str, user_id: str, updates: dict):
    client = _client(access_token)
    response = (
        client.table("diary_entries")
        .update(updates)
        .eq("id", entry_id)
        .eq("user_id", user_id)
        .execute()
    )
    return response.data[0] if response.data else None


def delete_entry(access_token: str, entry_id: str, user_id: str):
    client = _client(access_token)
    client.table("diary_entries").delete().eq("id", entry_id).eq("user_id", user_id).execute()
    return True
