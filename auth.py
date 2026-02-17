from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def sign_up(email, password):
    return supabase.auth.sign_up({"email": email, "password": password})


def sign_in(email, password):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


def sign_in_with_google():
    return supabase.auth.sign_in_with_oauth({
        "provider": "google"
    })


def get_user():
    return supabase.auth.get_user()


def sign_out():
    supabase.auth.sign_out()
