import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

def get_supabase():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )


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


def load_profile_from_db(user_id, access_token=None):
    """Loads profile from Supabase database"""
    try:
        from utils.supabase_client import get_profile
        return get_profile(user_id)
    except Exception as e:
        print(f"Error loading profile: {e}")
    return None


def check_session():
    """
    Restores session on every page load.
    Reads stored token from session_state and reloads profile.
    Returns True if logged in.
    """
    # Already fully loaded
    if st.session_state.get("user") and \
       st.session_state.get("profile") and \
       st.session_state.get("profile", {}).get("full_name"):
        return True

    # We have user but no profile — try loading from DB
    if st.session_state.get("user") and \
       st.session_state.get("access_token"):
        user = st.session_state.user
        token = st.session_state.access_token
        profile = load_profile_from_db(user.id, token)
        if profile and profile.get("full_name"):
            st.session_state.profile = profile
            return True

    return False


def require_login():
    """Redirects to login if not authenticated"""
    if not check_session():
        st.switch_page("pages/2_login.py")


def get_profile():
    return st.session_state.get("profile", {})


def get_user():
    return st.session_state.get("user", None)


def sign_out():
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.clear()