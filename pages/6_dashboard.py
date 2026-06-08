import streamlit as st
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

st.set_page_config(
    page_title="Dashboard — HackMate",
    page_icon="",
    layout="wide"
)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# ── STYLING ──────────────────────────────────────────
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0a0a0f; color: #ffffff; }

    .match-card {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.2s;
    }
    .match-card:hover { border-color: #6366f1; }

    .score-badge {
        background: #1e1b4b;
        color: #a78bfa;
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .skill-tag {
        background: #0d0d14;
        border: 1px solid #1f1f2e;
        color: #9ca3af;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-right: 4px;
    }

    .stat-card {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }

    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton > button:hover { background: #4f46e5; }
    </style>
""", unsafe_allow_html=True)


# ── AUTH CHECK ────────────────────────────────────────
# If not logged in send to login page
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import check_session, sign_out

check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")


# ── GET PROFILE ───────────────────────────────────────
profile = st.session_state.get("profile", {})
user = st.session_state.get("user", {})

# Fallback name if profile not set
name = profile.get("full_name", "Builder")
from utils.supabase_client import parse_list_field

skills = parse_list_field(profile.get("skills", []))
experience = profile.get("experience_level", "Intermediate")
availability = profile.get("availability", "3-5 hrs")
goals = parse_list_field(profile.get("goals", []))

# ── NAVBAR ────────────────────────────────────────────
from utils.supabase_client import get_my_requests

n1, n2, n3, n4 = st.columns([1, 3, 1, 1])
with n1:
    st.markdown(
        "<div class='hm-logo'>HackMate</div>",
        unsafe_allow_html=True
    )

# Get pending requests count
pending = []
if user:
    pending = get_my_requests(user.id)
notif_count = len(pending)

with n3:
    # Show notification badge
    if notif_count > 0:
        st.markdown(
            f"<div style='display:flex;align-items:center;"
            f"gap:8px;padding-top:0.3rem;'>"
            f"<div style='position:relative;display:inline-block;'>"
            f"<span style='font-size:0.82rem;color:#71717a;'>"
            f"Requests</span>"
            f"<span style='position:absolute;top:-6px;right:-14px;"
            f"background:#ef4444;color:white;"
            f"font-size:0.6rem;font-weight:600;"
            f"width:16px;height:16px;border-radius:50%;"
            f"display:flex;align-items:center;"
            f"justify-content:center;'>"
            f"{notif_count}</span>"
            f"</div></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='padding-top:0.3rem;"
            "font-size:0.82rem;color:#3f3f46;'>"
            "No requests</div>",
            unsafe_allow_html=True
        )
with n4:
    if st.button("Sign Out"):
        sign_out()
        st.switch_page("pages/2_login.py")


st.markdown("---")


# ── WELCOME SECTION ───────────────────────────────────
st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <h2 style='color:white; margin:0;'>
            Welcome back, {name}!
        </h2>
        <p style='color:#9ca3af; margin:0.3rem 0 0;'>
            Your AI-powered matches are ready.
        </p>
    </div>
""", unsafe_allow_html=True)


# ── STATS ROW ─────────────────────────────────────────
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("""
        <div class='stat-card'>
            <div style='font-size:2rem; font-weight:700;
                 color:#a78bfa;'>8</div>
            <div style='color:#6b7280; font-size:0.85rem;'>
                New Matches
            </div>
        </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
        <div class='stat-card'>
            <div style='font-size:2rem; font-weight:700;
                 color:#a78bfa;'>92%</div>
            <div style='color:#6b7280; font-size:0.85rem;'>
                Top Score
            </div>
        </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
        <div class='stat-card'>
            <div style='font-size:2rem; font-weight:700;
                 color:#a78bfa;'>3</div>
            <div style='color:#6b7280; font-size:0.85rem;'>
                Open Teams
            </div>
        </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size:2rem; font-weight:700;
                 color:#a78bfa;'>{len(skills)}</div>
            <div style='color:#6b7280; font-size:0.85rem;'>
                Your Skills
            </div>
        </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# ── SENT REQUESTS ─────────────────────────────────────
sent = st.session_state.get("sent_requests", [])
if sent:
    st.markdown(
        "<div class='hm-label'>Sent Requests</div>",
        unsafe_allow_html=True
    )
    for req in sent:
        status_color = (
            "#34d399" if req["status"] == "accepted"
            else "#f87171" if req["status"] == "declined"
            else "#71717a"
        )
        st.markdown(
            f"<div style='background:#111113;"
            f"border:1px solid #1c1c1f;"
            f"border-radius:12px;padding:1rem 1.2rem;"
            f"margin-bottom:0.5rem;"
            f"display:flex;justify-content:space-between;"
            f"align-items:center;'>"
            f"<div style='font-size:0.85rem;color:#a1a1aa;'>"
            f"Request to <span style='color:#f4f4f5;"
            f"font-family:Playfair Display,serif;'>"
            f"{req['to']}</span></div>"
            f"<span style='font-size:0.7rem;font-weight:500;"
            f"letter-spacing:0.08em;text-transform:uppercase;"
            f"color:{status_color};'>{req['status']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    st.markdown("<hr>", unsafe_allow_html=True)

# ── TEAM VOTE REQUESTS ────────────────────────────────
from utils.supabase_client import (
    get_pending_votes_for_user,
    cast_vote
)

if user:
    pending_votes = get_pending_votes_for_user(user.id)

    if pending_votes:
        st.markdown(
            "<div class='hm-label' "
            "style='margin-bottom:0.8rem;'>"
            "Team Vote Requests</div>",
            unsafe_allow_html=True
        )

        for vote in pending_votes:
            inv = vote.get("team_invitations", {})
            invitee_name = inv.get("invitee_name", "Someone")
            proposed_by = inv.get("proposed_by_name", "A teammate")
            invitation_id = vote.get("invitation_id")
            vote_id = vote.get("id")
            invitee_id = inv.get("invitee_id")

            st.markdown(
                f"<div style='background:#111113;"
                f"border:1px solid #1c1c1f;"
                f"border-radius:14px;padding:1.2rem 1.4rem;"
                f"margin-bottom:0.8rem;'>"
                f"<div style='font-size:0.68rem;font-weight:500;"
                f"letter-spacing:0.1em;text-transform:uppercase;"
                f"color:#3f3f46;margin-bottom:0.5rem;'>"
                f"Team Vote Required</div>"
                f"<div style='font-family:Playfair Display,serif;"
                f"font-size:0.95rem;color:#f4f4f5;"
                f"margin-bottom:0.3rem;'>"
                f"{proposed_by} wants to add "
                f"{invitee_name}</div>"
                f"<div style='font-size:0.78rem;color:#71717a;"
                f"font-style:italic;font-weight:300;'>"
                f"Vote to approve or reject this new "
                f"team member.</div>"
                f"</div>",
                unsafe_allow_html=True
            )

            vc1, vc2, vc3 = st.columns([2, 1, 1])

            with vc2:
                if st.button(
                    "Approve",
                    key=f"approve_vote_{vote_id}",
                    use_container_width=True
                ):
                    my_name = profile.get(
                        "full_name", "User"
                    )
                    result = cast_vote(
                        vote_id=vote_id,
                        invitation_id=invitation_id,
                        vote_value="accepted",
                        voter_id=user.id,
                        voter_name=my_name,
                        invitee_id=invitee_id,
                        invitee_name=invitee_name
                    )

                    if result == "approved":
                        st.success(
                            f"All approved! "
                            f"{invitee_name} is now "
                            f"part of your team!"
                        )
                    elif result == "vote_recorded":
                        st.success(
                            "Your vote recorded. "
                            "Waiting for other teammates."
                        )
                    st.rerun()

            with vc3:
                if st.button(
                    "Reject",
                    key=f"reject_vote_{vote_id}",
                    use_container_width=True
                ):
                    my_name = profile.get(
                        "full_name", "User"
                    )
                    cast_vote(
                        vote_id=vote_id,
                        invitation_id=invitation_id,
                        vote_value="rejected",
                        voter_id=user.id,
                        voter_name=my_name,
                        invitee_id=invitee_id,
                        invitee_name=invitee_name
                    )
                    st.info(
                        f"{invitee_name} was not added."
                    )
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

# ── INCOMING REQUESTS ─────────────────────────────────
from utils.supabase_client import get_my_requests, update_request_status

user = st.session_state.get("user")
if user:
    requests = get_my_requests(user.id)
    if requests:
        st.markdown(
            "<div class='hm-label' style='margin-bottom:0.8rem;'>"
            "Connection Requests</div>",
            unsafe_allow_html=True
        )
        for req in requests:
            rc1, rc2, rc3 = st.columns([3, 1, 1])
            with rc1:
                st.markdown(
                    f"<div style='background:#111113;"
                    f"border:1px solid #1c1c1f;"
                    f"border-radius:12px;padding:1rem 1.2rem;'>"
                    f"<div style='font-family:Playfair Display,serif;"
                    f"font-size:0.95rem;color:#f4f4f5;"
                    f"margin-bottom:0.3rem;'>"
                    f"{req.get('from_name', 'Someone')} "
                    f"wants to team up</div>"
                    f"<div style='font-size:0.8rem;color:#71717a;"
                    f"font-style:italic;font-weight:300;'>"
                    f"{req.get('message', 'No message')}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with rc2:
                if st.button(
                    "Accept",
                    key=f"accept_{req['id']}",
                    use_container_width=True
                ):
                    update_request_status(req["id"], "accepted")

                    # Create team connection
                    from utils.supabase_client import (
                        create_team_connection
                    )
                    my_name = profile.get(
                        "full_name", "User"
                    )
                    create_team_connection(
                        user1_id=user.id,
                        user2_id=req["from_user_id"],
                        user1_name=my_name,
                        user2_name=req.get("from_name", "User")
                    )
                    st.success(
                        f"Connected with "
                        f"{req.get('from_name')}! "
                        f"Check Team Workspace."
                    )
                    st.rerun()
            with rc3:
                if st.button(
                    "Decline",
                    key=f"decline_{req['id']}",
                    use_container_width=True
                ):
                    update_request_status(req["id"], "declined")
                    st.info("Request declined.")
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────
left, right = st.columns([2, 1])


# ── LEFT: AI MATCHES ──────────────────────────────────
with left:
    st.markdown("### 🤖 Top AI Matches For You")
    st.markdown(
        "<small style='color:#6b7280'>Based on your skills, "
        "experience and goals</small>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Sample matches — we replace with real AI later
    matches = [
        {
            "name": "Arjun Mehta",
            "skills": ["Machine Learning", "Python", "TensorFlow"],
            "experience": "Advanced",
            "availability": "Full time",
            "goals": ["Win prizes"],
            "score": 92,
            "reason": "Complements your frontend skills with strong ML backend"
        },
        {
            "name": "Priya Sharma",
            "skills": ["UI/UX Design", "Figma", "React"],
            "experience": "Intermediate",
            "availability": "6-8 hrs",
            "goals": ["Build portfolio"],
            "score": 87,
            "reason": "Brings design skills your team is missing"
        },
        {
            "name": "Rahul Dev",
            "skills": ["Node.js", "MongoDB", "DevOps"],
            "experience": "Intermediate",
            "availability": "3-5 hrs",
            "goals": ["Learn new tech"],
            "score": 81,
            "reason": "Strong backend skills to balance your team"
        },
        {
            "name": "Sneha Patel",
            "skills": ["Data Science", "SQL", "Tableau"],
            "experience": "Beginner",
            "availability": "3-5 hrs",
            "goals": ["Network", "Learn new tech"],
            "score": 74,
            "reason": "Data skills add analytics capability to your project"
        },
    ]

    for match in matches:
        # Build skills tags HTML
        skill_tags = "".join([
            f"<span class='skill-tag'>{s}</span>"
            for s in match["skills"]
        ])

        st.markdown(f"""
            <div class='match-card'>
                <div style='display:flex; justify-content:space-between;
                     align-items:start; margin-bottom:0.6rem;'>
                    <div>
                        <div style='font-weight:600; font-size:1rem;
                             color:white;'>
                            {match["name"]}
                        </div>
                        <div style='color:#6b7280; font-size:0.82rem;
                             margin-top:2px;'>
                            {match["experience"]} · {match["availability"]}
                        </div>
                    </div>
                    <span class='score-badge'>{match["score"]}% Match</span>
                </div>
                <div style='margin-bottom:0.6rem;'>{skill_tags}</div>
                <div style='color:#6366f1; font-size:0.82rem;
                     background:#0d0f1f; padding:6px 10px;
                     border-radius:6px;'>
                    ✦ {match["reason"]}
                </div>
            </div>
        """, unsafe_allow_html=True)


# ── RIGHT SIDEBAR ─────────────────────────────────────
with right:

    # Your profile summary
    st.markdown("### Your Profile")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── TEAM MEMBERS PREVIEW ──────────────────────────
    from utils.supabase_client import get_team_members

    team_members = get_team_members(user.id)

    st.markdown(
        "<div class='hm-label'>Your Team</div>",
        unsafe_allow_html=True
    )

    if team_members:
        for member in team_members:
            initial = member["name"][0].upper()
            st.markdown(
                f"<div style='background:#111113;"
                f"border:1px solid #1c1c1f;"
                f"border-radius:12px;padding:1rem 1.2rem;"
                f"margin-bottom:0.5rem;"
                f"display:flex;align-items:center;gap:1rem;'>"
                f"<div style='width:36px;height:36px;"
                f"border-radius:8px;background:#18181b;"
                f"border:1px solid #27272a;"
                f"display:flex;align-items:center;"
                f"justify-content:center;"
                f"font-family:Playfair Display,serif;"
                f"color:#a1a1aa;font-size:0.9rem;'>"
                f"{initial}</div>"
                f"<div>"
                f"<div style='font-family:Playfair Display,serif;"
                f"font-size:0.9rem;color:#f4f4f5;'>"
                f"{member['name']}</div>"
                f"<div style='font-size:0.7rem;color:#52525b;"
                f"letter-spacing:0.04em;'>Team member</div>"
                f"</div></div>",
                unsafe_allow_html=True
            )

        if st.button(
            "Open Team Workspace",
            use_container_width=True
        ):
            st.switch_page("pages/7_team_workspace.py")

    else:
        st.markdown(
            "<div style='background:#111113;"
            "border:1px solid #1c1c1f;"
            "border-radius:12px;padding:1.2rem;"
            "font-size:0.82rem;color:#52525b;"
            "font-style:italic;font-weight:300;'>"
            "No team members yet. Find teammates and "
            "send connection requests to build your team."
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div style='height:1.5rem'></div>",
        unsafe_allow_html=True
    )
    
    st.markdown(f"""
        <div style='background:#13131a; border:1px solid #1f1f2e;
             border-radius:12px; padding:1.2rem;'>
            <div style='font-weight:600; color:white;
                 margin-bottom:0.3rem;'>{name}</div>
            <div style='color:#6b7280; font-size:0.82rem;
                 margin-bottom:0.8rem;'>{experience} · {availability}/day</div>
            <div style='color:#9ca3af; font-size:0.82rem;
                 margin-bottom:0.4rem;'>Skills</div>
            <div>{"".join([f"<span class='skill-tag'>{s}</span>"
                 for s in skills]) if skills
                 else "<span style='color:#6b7280'>No skills added yet</span>"}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick actions
    st.markdown("### Quick Actions")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Find Teammates", use_container_width=True):
        st.switch_page("pages/4_find_teammates.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Project Idea", use_container_width=True):
        st.switch_page("pages/5_match_results.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Team Workspace", use_container_width=True):
        st.switch_page("pages/7_team_workspace.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Edit Profile", use_container_width=True):
        st.switch_page("pages/8_edit_profile.py")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Goals display
    if goals:
        st.markdown("### Your Goals")
        st.markdown("<br>", unsafe_allow_html=True)
        for goal in goals:
            st.markdown(f"""
                <div style='background:#13131a; border:1px solid #1f1f2e;
                     border-radius:8px; padding:0.5rem 0.8rem;
                     color:#9ca3af; font-size:0.82rem;
                     margin-bottom:0.4rem;'>
                    ✦ {goal}
                </div>
            """, unsafe_allow_html=True)