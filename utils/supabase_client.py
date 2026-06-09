from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()


def get_admin_client():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )


def get_client():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )


def parse_list_field(value):
    """Safely parses a field that should be a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        import json
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
        if value.strip():
            return [value]
    return []


def save_profile(user_id, profile_data, access_token=None):
    """Save or update a user profile in Supabase"""
    try:
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
            "availability": profile_data.get(
                "availability", "3-5 hrs"
            ),
            "goals": profile_data.get("goals", []),
        }).execute()
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


# ── CONNECTION REQUESTS ───────────────────────────────

def send_request(from_user_id, to_user_id,
                 from_name, message=""):
    """Send a direct connection request"""
    try:
        client = get_admin_client()
        existing = client.table("requests")\
            .select("*")\
            .eq("from_user_id", from_user_id)\
            .eq("to_user_id", to_user_id)\
            .execute()
        if existing.data:
            return "already_sent"
        client.table("requests").insert({
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
    """Get all incoming connection requests"""
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
    """Accept or decline a connection request"""
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


# ── TEAM CONNECTIONS ──────────────────────────────────

def create_team_connection(user1_id, user2_id,
                            user1_name, user2_name):
    """Creates a team connection between two users"""
    try:
        client = get_admin_client()
        u1 = str(user1_id)
        u2 = str(user2_id)

        if u1.startswith("sample-") or \
           u2.startswith("sample-"):
            return False

        # Check both directions
        e1 = client.table("team_connections")\
            .select("id")\
            .eq("user1_id", u1)\
            .eq("user2_id", u2)\
            .execute()
        e2 = client.table("team_connections")\
            .select("id")\
            .eq("user1_id", u2)\
            .eq("user2_id", u1)\
            .execute()

        if e1.data or e2.data:
            print(f"Already connected: {u1} — {u2}")
            return True

        client.table("team_connections").insert({
            "user1_id": u1,
            "user2_id": u2,
            "user1_name": user1_name,
            "user2_name": user2_name
        }).execute()

        print(f"Connected: {user1_name} — {user2_name}")
        return True

    except Exception as e:
        print(f"Error creating connection: {e}")
        return False


def get_team_members(user_id):
    """Get all people connected with this user"""
    try:
        client = get_admin_client()
        uid = str(user_id)

        response = client.table("team_connections")\
            .select("*")\
            .or_(
                f"user1_id.eq.{uid},"
                f"user2_id.eq.{uid}"
            ).execute()

        members = []
        for conn in response.data or []:
            if str(conn["user1_id"]) == uid:
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


# ── TEAM INVITATIONS ──────────────────────────────────

def send_team_invite(proposer_id, proposer_name,
                     invitee_id, invitee_name):
    """
    Step 1: Proposer invites invitee.
    Invitee must accept before team votes.
    """
    try:
        client = get_admin_client()
        uid = str(invitee_id)

        if uid.startswith("sample-"):
            return "sample_profile"

        # Check if already invited
        existing = client.table("team_invitations")\
            .select("id")\
            .eq("proposer_id", proposer_id)\
            .eq("invitee_id", uid)\
            .in_("status", [
                "pending_acceptance", "voting"
            ])\
            .execute()

        if existing.data:
            return "already_invited"

        client.table("team_invitations").insert({
            "invitee_id": uid,
            "invitee_name": invitee_name,
            "proposer_id": proposer_id,
            "proposer_name": proposer_name,
            "status": "pending_acceptance"
        }).execute()

        return "invite_sent"

    except Exception as e:
        print(f"Error sending invite: {e}")
        return "error"


def get_incoming_invites(user_id):
    """
    Get all team invitations where this user
    is the invitee and status is pending_acceptance.
    """
    try:
        client = get_admin_client()
        uid = str(user_id)

        response = client.table("team_invitations")\
            .select("*")\
            .eq("invitee_id", uid)\
            .eq("status", "pending_acceptance")\
            .execute()

        return response.data or []

    except Exception as e:
        print(f"Error getting invites: {e}")
        return []


def respond_to_invite(invitation_id, accepted,
                      proposer_id):
    """
    Step 2: Invitee accepts or declines.
    If accepted → create vote requests for team members.
    """
    try:
        client = get_admin_client()

        if not accepted:
            client.table("team_invitations")\
                .update({"status": "declined"})\
                .eq("id", invitation_id)\
                .execute()
            return "declined"

        # Get invitation details
        inv = client.table("team_invitations")\
            .select("*")\
            .eq("id", invitation_id)\
            .execute()

        if not inv.data:
            return "error"

        # Update status to voting
        client.table("team_invitations")\
            .update({"status": "voting"})\
            .eq("id", invitation_id)\
            .execute()

        # Get all current team members of proposer
        team_members = get_team_members(proposer_id)

        if not team_members:
            # No other members — approve directly
            inv_data = inv.data[0]
            create_team_connection(
                user1_id=proposer_id,
                user2_id=inv_data["invitee_id"],
                user1_name=inv_data["proposer_name"],
                user2_name=inv_data["invitee_name"]
            )
            client.table("team_invitations")\
                .update({"status": "approved"})\
                .eq("id", invitation_id)\
                .execute()
            return "approved_directly"

        # Create vote for each team member
        for member in team_members:
            client.table("team_votes").insert({
                "invitation_id": invitation_id,
                "voter_id": member["id"],
                "voter_name": member["name"],
                "vote": "pending"
            }).execute()

        return "voting_started"

    except Exception as e:
        print(f"Error responding to invite: {e}")
        return "error"


def get_pending_votes_for_user(user_id):
    """Get all invitations where this user needs to vote."""
    try:
        client = get_admin_client()
        uid = str(user_id)

        votes = client.table("team_votes")\
            .select("*")\
            .eq("voter_id", uid)\
            .eq("vote", "pending")\
            .execute()

        if not votes.data:
            return []

        result = []
        for vote in votes.data:
            inv = client.table("team_invitations")\
                .select("*")\
                .eq("id", vote["invitation_id"])\
                .eq("status", "voting")\
                .execute()
            if inv.data:
                vote["team_invitations"] = inv.data[0]
                result.append(vote)

        return result

    except Exception as e:
        print(f"Error getting votes: {e}")
        return []


def cast_vote(vote_id, invitation_id,
              vote_value, voter_id, voter_name,
              invitee_id, invitee_name):
    """
    Step 3: Team member votes.
    If all accept → add invitee to ALL members' teams.
    If anyone rejects → close invitation.
    """
    try:
        client = get_admin_client()

        # Record vote
        client.table("team_votes")\
            .update({
                "vote": vote_value,
                "voted_at": "now()"
            })\
            .eq("id", vote_id)\
            .execute()

        if vote_value == "rejected":
            client.table("team_invitations")\
                .update({"status": "rejected"})\
                .eq("id", invitation_id)\
                .execute()
            return "rejected"

        # Check if all votes are accepted
        all_votes = client.table("team_votes")\
            .select("*")\
            .eq("invitation_id", invitation_id)\
            .execute()

        votes_list = all_votes.data or []
        all_accepted = all(
            v["vote"] == "accepted"
            for v in votes_list
        )

        if not all_accepted:
            return "vote_recorded"

        # All accepted — get invitation details
        inv = client.table("team_invitations")\
            .select("*")\
            .eq("id", invitation_id)\
            .execute()

        if not inv.data:
            return "error"

        inv_data = inv.data[0]
        proposer_id = inv_data["proposer_id"]
        real_invitee_id = inv_data["invitee_id"]
        real_invitee_name = inv_data["invitee_name"]

        # Get proposer name
        proposer = client.table("profiles")\
            .select("full_name")\
            .eq("id", proposer_id)\
            .execute()
        proposer_name = proposer.data[0]["full_name"] \
            if proposer.data else "User"

        # Get ALL team members of proposer
        all_members = get_team_members(proposer_id)

        # Connect invitee with proposer
        create_team_connection(
            user1_id=proposer_id,
            user2_id=real_invitee_id,
            user1_name=proposer_name,
            user2_name=real_invitee_name
        )

        # Connect invitee with EVERY team member
        for member in all_members:
            if str(member["id"]) != str(real_invitee_id):
                create_team_connection(
                    user1_id=member["id"],
                    user2_id=real_invitee_id,
                    user1_name=member["name"],
                    user2_name=real_invitee_name
                )

        # Mark approved
        client.table("team_invitations")\
            .update({"status": "approved"})\
            .eq("id", invitation_id)\
            .execute()

        return "approved"

    except Exception as e:
        print(f"Error casting vote: {e}")
        return "error"


def get_invitation_status(proposer_id, invitee_id):
    """Check if an active invitation exists"""
    try:
        client = get_admin_client()
        result = client.table("team_invitations")\
            .select("*")\
            .eq("proposer_id", proposer_id)\
            .eq("invitee_id", str(invitee_id))\
            .in_("status", [
                "pending_acceptance", "voting"
            ])\
            .execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error checking invitation: {e}")
        return None

def send_team_message(sender_id, sender_name,
                      team_member_ids, message):
    """Save a message to Supabase"""
    try:
        client = get_admin_client()

        # Build list of all people who can see this
        # message (sender + all team members)
        all_ids = [str(sender_id)] + [
            str(mid) for mid in team_member_ids
        ]

        client.table("team_messages").insert({
            "sender_id": str(sender_id),
            "sender_name": sender_name,
            "recipient_ids": all_ids,
            "message": message
        }).execute()

        return True

    except Exception as e:
        print(f"Error sending message: {e}")
        return False


def get_team_messages(user_id, limit=50):
    """
    Get all messages where this user is
    sender or recipient.
    """
    try:
        client = get_admin_client()
        uid = str(user_id)

        # Get messages where user is in recipient_ids
        response = client.table("team_messages")\
            .select("*")\
            .contains("recipient_ids", [uid])\
            .order("created_at", desc=False)\
            .limit(limit)\
            .execute()

        return response.data or []

    except Exception as e:
        print(f"Error getting messages: {e}")
        return []
    
def add_team_task(created_by_id, created_by_name,
                  team_member_ids, task_text,
                  assigned_to):
    """Add a new task visible to all team members"""
    try:
        client = get_admin_client()

        all_ids = [str(created_by_id)] + [
            str(mid) for mid in team_member_ids
        ]

        client.table("team_tasks").insert({
            "created_by_id": str(created_by_id),
            "created_by_name": created_by_name,
            "team_member_ids": all_ids,
            "task_text": task_text,
            "assigned_to": assigned_to,
            "status": "todo"
        }).execute()

        return True

    except Exception as e:
        print(f"Error adding task: {e}")
        return False


def get_team_tasks(user_id):
    """Get all tasks visible to this user"""
    try:
        client = get_admin_client()
        uid = str(user_id)

        response = client.table("team_tasks")\
            .select("*")\
            .contains("team_member_ids", [uid])\
            .order("created_at", desc=False)\
            .execute()

        return response.data or []

    except Exception as e:
        print(f"Error getting tasks: {e}")
        return []


def update_task_status(task_id, new_status):
    """Move task to new status"""
    try:
        client = get_admin_client()
        client.table("team_tasks")\
            .update({"status": new_status})\
            .eq("id", task_id)\
            .execute()
        return True
    except Exception as e:
        print(f"Error updating task: {e}")
        return False


def delete_team_task(task_id):
    """Delete a task"""
    try:
        client = get_admin_client()
        client.table("team_tasks")\
            .delete()\
            .eq("id", task_id)\
            .execute()
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False