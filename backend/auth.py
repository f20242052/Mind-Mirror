from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_ANON_KEY


def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def register(email: str, password: str):
    client = get_client()
    response = client.auth.sign_up({"email": email, "password": password})
    return response


def login(email: str, password: str):
    client = get_client()
    response = client.auth.sign_in_with_password({"email": email, "password": password})
    return response


def logout(access_token: str):
    client = get_client()
    client.auth.sign_out()


def get_user(access_token: str):
    client = get_client()
    client.auth.session = {"access_token": access_token}
    return client.auth.get_user(access_token)
