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

def send_request(from_user_id, to_user_id, from_name, message=""):
    """Send a connection request to another user"""
    try:
        client = get_admin_client()

        # Check if request already exists
        existing = client.table("requests")\
            .select("*")\
            .eq("from_user_id", from_user_id)\
            .eq("to_user_id", to_user_id)\
            .execute()

        if existing.data:
            return "already_sent"

        response = client.table("requests").insert({
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "from_name": from_name,
            "message": message,
            "status": "pending"
        }).execute()

        return "sent"

    except Exception as e:
        print(f"Error sending request: {e}")
        return "error"


def get_my_requests(user_id):
    """Get all incoming requests for a user"""
    try:
        client = get_admin_client()
        response = client.table("requests")\
            .select("*")\
            .eq("to_user_id", user_id)\
            .eq("status", "pending")\
            .execute()
        return response.data or []
    except Exception as e:
        print(f"Error getting requests: {e}")
        return []


def update_request_status(request_id, status):
    """Accept or decline a request"""
    try:
        client = get_admin_client()
        client.table("requests")\
            .update({"status": status})\
            .eq("id", request_id)\
            .execute()
        return True
    except Exception as e:
        print(f"Error updating request: {e}")
        return False
    
def create_team_connection(user1_id, user2_id,
                           user1_name, user2_name):
    """Creates a team connection when request is accepted"""
    try:
        client = get_admin_client()

        # Check if already connected
        existing = client.table("team_connections")\
            .select("*")\
            .or_(
                f"and(user1_id.eq.{user1_id},"
                f"user2_id.eq.{user2_id}),"
                f"and(user1_id.eq.{user2_id},"
                f"user2_id.eq.{user1_id})"
            ).execute()

        if existing.data:
            return True

        client.table("team_connections").insert({
            "user1_id": user1_id,
            "user2_id": user2_id,
            "user1_name": user1_name,
            "user2_name": user2_name
        }).execute()

        return True
    except Exception as e:
        print(f"Error creating connection: {e}")
        return False


def get_team_members(user_id):
    """Get all people connected with this user"""
    try:
        client = get_admin_client()
        response = client.table("team_connections")\
            .select("*")\
            .or_(
                f"user1_id.eq.{user_id},"
                f"user2_id.eq.{user_id}"
            ).execute()

        members = []
        for conn in response.data or []:
            if conn["user1_id"] == user_id:
                members.append({
                    "name": conn["user2_name"],
                    "id": conn["user2_id"],
                    "connected_at": conn["connected_at"]
                })
            else:
                members.append({
                    "name": conn["user1_name"],
                    "id": conn["user1_id"],
                    "connected_at": conn["connected_at"]
                })
        return members
    except Exception as e:
        print(f"Error getting team members: {e}")
        return []