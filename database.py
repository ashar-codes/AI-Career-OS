from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_resume(user_id, title, content):
    supabase.table("resumes").insert({
        "user_id": user_id,
        "title": title,
        "content": content
    }).execute()


def get_user_resumes(user_id):
    response = supabase.table("resumes").select("*").eq("user_id", user_id).execute()
    return response.data
