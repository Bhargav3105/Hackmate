from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()


def get_admin_client():
    """
    Uses service role key — bypasses RLS.
    Only use this for server-side operations like saving profiles.
    Never expose this key to users.
    """
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )


def get_client():
    """Regular anon client for normal reads"""
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )


def save_profile(user_id, profile_data, access_token=None):
    """Save or update a user profile in Supabase"""
    try:
        # Use admin client to bypass RLS
        client = get_admin_client()

        response = client.table("profiles").upsert({
            "id": user_id,
            "full_name": profile_data.get("full_name"),
            "github_url": profile_data.get("github_url", ""),
            "bio": profile_data.get("bio", ""),
            "skills": profile_data.get("skills", []),
            "experience_level": profile_data.get(
                "experience_level", "Intermediate"
            ),
            "availability": profile_data.get("availability", "3-5 hrs"),
            "goals": profile_data.get("goals", []),
        }).execute()

        print(f"Profile saved: {response.data}")
        return response

    except Exception as e:
        print(f"Error saving profile: {e}")
        return None


def get_profile(user_id):
    """Get a user profile from Supabase"""
    try:
        client = get_admin_client()
        response = client.table("profiles")\
            .select("*")\
            .eq("id", user_id)\
            .execute()

        if response.data:
            return response.data[0]
        return None

    except Exception as e:
        print(f"Error getting profile: {e}")
        return None


def get_all_profiles(exclude_user_id=None):
    """Get all profiles except the current user"""
    try:
        client = get_admin_client()
        query = client.table("profiles").select("*")

        if exclude_user_id:
            query = query.neq("id", exclude_user_id)

        response = query.execute()
        return response.data or []

    except Exception as e:
        print(f"Error getting profiles: {e}")
        return []

def parse_list_field(value):
    """
    Safely parses a field that should be a list.
    Handles strings, JSON strings, and actual lists.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        import json
        # Try JSON parse first
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
        # If it looks like a plain string, wrap it
        if value.strip():
            return [value]
    return []