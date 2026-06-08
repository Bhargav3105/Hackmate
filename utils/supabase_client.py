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
        u1 = str(user1_id)
        u2 = str(user2_id)

        # Don't connect sample profiles
        if u1.startswith("sample-") or \
           u2.startswith("sample-"):
            return False

        # Check if already connected using two queries
        existing1 = client.table("team_connections")\
            .select("id")\
            .eq("user1_id", u1)\
            .eq("user2_id", u2)\
            .execute()

        existing2 = client.table("team_connections")\
            .select("id")\
            .eq("user1_id", u2)\
            .eq("user2_id", u1)\
            .execute()

        if existing1.data or existing2.data:
            print(f"Already connected: {u1} - {u2}")
            return True

        # Create the connection
        client.table("team_connections").insert({
            "user1_id": u1,
            "user2_id": u2,
            "user1_name": user1_name,
            "user2_name": user2_name
        }).execute()

        print(f"Created connection: {user1_name} — {user2_name}")
        return True

    except Exception as e:
        print(f"Error creating connection: {e}")
        return False


def get_team_members(user_id):
    """Get all people connected with this user"""
    try:
        client = get_admin_client()
        user_id_str = str(user_id)

        response = client.table("team_connections")\
            .select("*")\
            .or_(
                f"user1_id.eq.{user_id_str},"
                f"user2_id.eq.{user_id_str}"
            ).execute()

        members = []
        for conn in response.data or []:
            # Always compare as strings
            if str(conn["user1_id"]) == user_id_str:
                members.append({
                    "name": conn["user2_name"],
                    "id": str(conn["user2_id"]),
                    "connected_at": conn["connected_at"]
                })
            else:
                members.append({
                    "name": conn["user1_name"],
                    "id": str(conn["user1_id"]),
                    "connected_at": conn["connected_at"]
                })

        return members

    except Exception as e:
        print(f"Error getting team members: {e}")
        return []

def propose_team_member(
    invitee_id, invitee_name,
    proposed_by_id, proposed_by_name
):
    """
    Proposes adding someone to the team.
    Creates invitation + vote requests for all
    existing team members.
    """
    try:
        client = get_admin_client()

        # Get all current team members of proposer
        current_members = get_team_members(proposed_by_id)

        # If no teammates yet, just add directly
        if not current_members:
            create_team_connection(
                user1_id=proposed_by_id,
                user2_id=invitee_id,
                user1_name=proposed_by_name,
                user2_name=invitee_name
            )
            return "added_directly"

        # Create invitation record
        inv = client.table("team_invitations").insert({
            "invitee_id": str(invitee_id),
            "invitee_name": invitee_name,
            "proposed_by_id": proposed_by_id,
            "proposed_by_name": proposed_by_name,
            "anchor_user_id": proposed_by_id,
            "status": "voting"
        }).execute()

        invitation_id = inv.data[0]["id"]

        # Create vote for each existing team member
        # (proposer auto-votes accept)
        for member in current_members:
            client.table("team_votes").insert({
                "invitation_id": invitation_id,
                "voter_id": member["id"],
                "voter_name": member["name"],
                "vote": "pending"
            }).execute()

        return "voting_started"

    except Exception as e:
        print(f"Error proposing member: {e}")
        return "error"


def get_pending_votes_for_user(user_id):
    """
    Get all invitations where this user needs to vote.
    """
    try:
        client = get_admin_client()

        # Get all pending votes for this user
        votes = client.table("team_votes")\
            .select("*, team_invitations(*)")\
            .eq("voter_id", user_id)\
            .eq("vote", "pending")\
            .execute()

        return votes.data or []

    except Exception as e:
        print(f"Error getting votes: {e}")
        return []


def cast_vote(vote_id, invitation_id,
              vote_value, voter_id, voter_name,
              invitee_id, invitee_name):
    """
    Cast a vote. If all votes accepted → add to team.
    If any rejected → reject invitation.
    """
    try:
        client = get_admin_client()

        # Record this vote
        client.table("team_votes")\
            .update({
                "vote": vote_value,
                "voted_at": "now()"
            })\
            .eq("id", vote_id)\
            .execute()

        # If rejected — close invitation immediately
        if vote_value == "rejected":
            client.table("team_invitations")\
                .update({"status": "rejected"})\
                .eq("id", invitation_id)\
                .execute()
            return "rejected"

        # Check if ALL votes are now accepted
        all_votes = client.table("team_votes")\
            .select("*")\
            .eq("invitation_id", invitation_id)\
            .execute()

        votes_list = all_votes.data or []
        all_accepted = all(
            v["vote"] == "accepted"
            for v in votes_list
        )

        if all_accepted:
            # Get invitation details
            inv = client.table("team_invitations")\
                .select("*")\
                .eq("id", invitation_id)\
                .execute()

            if inv.data:
                inv_data = inv.data[0]
                anchor_id = inv_data["anchor_user_id"]

                # Get anchor user name
                anchor = client.table("profiles")\
                    .select("full_name")\
                    .eq("id", anchor_id)\
                    .execute()

                anchor_name = anchor.data[0]["full_name"] \
                    if anchor.data else "User"

                # Add invitee to team
                create_team_connection(
                    user1_id=anchor_id,
                    user2_id=invitee_id,
                    user1_name=anchor_name,
                    user2_name=invitee_name
                )

                # Mark invitation as approved
                client.table("team_invitations")\
                    .update({"status": "approved"})\
                    .eq("id", invitation_id)\
                    .execute()

                return "approved"

        return "vote_recorded"

    except Exception as e:
        print(f"Error casting vote: {e}")
        return "error"


def get_invitation_status(proposed_by_id, invitee_id):
    """Check if an invitation already exists"""
    try:
        client = get_admin_client()
        result = client.table("team_invitations")\
            .select("*")\
            .eq("proposed_by_id", proposed_by_id)\
            .eq("invitee_id", str(invitee_id))\
            .eq("status", "voting")\
            .execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error checking invitation: {e}")
        return None