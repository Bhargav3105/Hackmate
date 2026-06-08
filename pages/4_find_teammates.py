import streamlit as st
from dotenv import load_dotenv
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ai_helper import calculate_compatibility
from utils.auth import check_session
from utils.styles import load_css
from utils.supabase_client import (
    get_all_profiles, get_team_members,
    propose_team_member, get_invitation_status,
    parse_list_field
)

load_dotenv()

st.set_page_config(
    page_title="Find Teammates — HackMate",
    page_icon="H",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

# ── SESSION CHECK ─────────────────────────────────────
check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")

user = st.session_state.get("user")
user_profile = st.session_state.get("profile", {})

if not user_profile:
    st.warning("Complete your profile first.")
    if st.button("Set Up Profile"):
        st.switch_page("pages/3_profile_setup.py")
    st.stop()

# Fix list fields
user_profile["skills"] = parse_list_field(
    user_profile.get("skills", [])
)
user_profile["goals"] = parse_list_field(
    user_profile.get("goals", [])
)

# ── LOAD REAL TEAM MEMBERS ────────────────────────────
real_members = get_team_members(user.id) if user else []
member_ids = [m["id"] for m in real_members]

# ── LOAD ALL PROFILES ─────────────────────────────────
real_profiles = get_all_profiles(
    exclude_user_id=user.id if user else None
)

sample_profiles = [
    {
        "id": "sample-001",
        "full_name": "Arjun Mehta",
        "skills": ["Machine Learning", "Python",
                   "TensorFlow", "FastAPI"],
        "experience_level": "Advanced",
        "availability": "Full time",
        "goals": ["Win prizes", "Launch a startup"],
        "bio": "ML engineer who loves building AI products.",
        "github_url": "https://github.com/arjunmehta"
    },
    {
        "id": "sample-002",
        "full_name": "Priya Sharma",
        "skills": ["UI/UX Design", "Figma",
                   "React", "JavaScript"],
        "experience_level": "Intermediate",
        "availability": "6-8 hrs",
        "goals": ["Build my portfolio",
                  "Learn new technologies"],
        "bio": "Designer who codes.",
        "github_url": "https://github.com/priyasharma"
    },
    {
        "id": "sample-003",
        "full_name": "Rahul Dev",
        "skills": ["Node.js", "MongoDB",
                   "DevOps", "Docker"],
        "experience_level": "Intermediate",
        "availability": "3-5 hrs",
        "goals": ["Learn new technologies",
                  "Network with developers"],
        "bio": "Backend developer obsessed with scale.",
        "github_url": "https://github.com/rahuldev"
    },
]

all_profiles = real_profiles if real_profiles else sample_profiles

# ── NAV ───────────────────────────────────────────────
st.markdown(
    "<div style='height:32px'></div>",
    unsafe_allow_html=True
)

n1, n2, n3 = st.columns([1, 5, 1])
with n1:
    st.markdown(
        "<div class='hm-logo'>HackMate</div>",
        unsafe_allow_html=True
    )
with n3:
    if st.button("Dashboard"):
        st.switch_page("pages/6_dashboard.py")

st.markdown("<hr>", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────
st.markdown(
    "<div style='margin-bottom:2rem;'>"
    "<div class='hm-label'>AI Powered</div>"
    "<div class='hm-title'>Find Teammates</div>"
    "<div style='font-size:0.85rem;color:#52525b;"
    "margin-top:0.5rem;font-weight:300;'>"
    "Check compatibility and invite developers to your team."
    "</div></div>",
    unsafe_allow_html=True
)

# ── SOURCE INDICATOR ──────────────────────────────────
if real_profiles:
    st.markdown(
        f"<div style='font-size:0.75rem;color:#34d399;"
        f"margin-bottom:1rem;'>"
        f"{len(real_profiles)} real developer"
        f"{'s' if len(real_profiles) != 1 else ''} "
        f"on HackMate</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div style='font-size:0.75rem;color:#52525b;"
        "margin-bottom:1rem;'>"
        "Showing sample profiles — invite friends to "
        "join HackMate to see real matches.</div>",
        unsafe_allow_html=True
    )

# ── FILTERS ───────────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Filter</div>",
    unsafe_allow_html=True
)

sc1, sc2, sc3 = st.columns(3)

with sc1:
    search_name = st.text_input(
        "Search",
        placeholder="Search by name...",
        label_visibility="collapsed"
    )

with sc2:
    filter_exp = st.multiselect(
        "Experience Level",
        options=["Beginner", "Intermediate", "Advanced"]
    )

with sc3:
    filter_avail = st.multiselect(
        "Availability",
        options=["1-2 hrs", "3-5 hrs", "6-8 hrs", "Full time"]
    )

# Apply filters
filtered = all_profiles

if search_name:
    filtered = [
        p for p in filtered
        if search_name.lower() in
        p.get("full_name", "").lower()
    ]
if filter_exp:
    filtered = [
        p for p in filtered
        if p["experience_level"] in filter_exp
    ]
if filter_avail:
    filtered = [
        p for p in filtered
        if p["availability"] in filter_avail
    ]

st.markdown(
    f"<div style='font-size:0.75rem;color:#3f3f46;"
    f"margin:1rem 0;'>"
    f"{len(filtered)} candidates</div>",
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# ── CANDIDATE CARDS ───────────────────────────────────
for profile in filtered:
    safe_key = profile["full_name"].replace(" ", "_")

    skill_tags = "".join([
        f"<span class='hm-tag'>{s}</span>"
        for s in profile["skills"]
    ])

    # Check relationship status
    already_in_team = profile["id"] in member_ids

    existing_inv = get_invitation_status(
        user.id, profile["id"]
    ) if user and profile["id"] != "sample-001" \
        and profile["id"] != "sample-002" \
        and profile["id"] != "sample-003" else None

    # ── CARD ──────────────────────────────────────────
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown(
            f"<div style='font-family:Playfair Display,serif;"
            f"font-size:1.05rem;font-weight:500;color:#f4f4f5;"
            f"margin-bottom:2px;'>{profile['full_name']}</div>"
            f"<div style='font-size:0.75rem;color:#52525b;"
            f"margin-bottom:0.5rem;'>"
            f"{profile['experience_level']} · "
            f"{profile['availability']}/day</div>"
            f"<div style='font-size:0.82rem;color:#71717a;"
            f"font-style:italic;margin-bottom:0.6rem;'>"
            f"{profile.get('bio', '')}</div>"
            f"<div>{skill_tags}</div>",
            unsafe_allow_html=True
        )

    with col2:
        check = st.button(
            "Check Compatibility",
            key=f"check_{safe_key}",
            use_container_width=True
        )

    with col3:
        if already_in_team:
            st.markdown(
                "<div style='font-size:0.72rem;color:#34d399;"
                "padding:0.6rem 0;text-align:center;"
                "letter-spacing:0.05em;'>In Your Team</div>",
                unsafe_allow_html=True
            )
        elif existing_inv:
            st.markdown(
                "<div style='font-size:0.72rem;color:#a1a1aa;"
                "padding:0.6rem 0;text-align:center;"
                "letter-spacing:0.05em;'>Vote Pending</div>",
                unsafe_allow_html=True
            )
        else:
            invite = st.button(
                "Invite to Team",
                key=f"connect_{safe_key}",
                use_container_width=True
            )
            if invite:
                st.session_state[
                    f"show_msg_{safe_key}"
                ] = True

    # ── COMPATIBILITY RESULT ──────────────────────────
    if check:
        with st.spinner(
            f"Calculating compatibility with "
            f"{profile['full_name']}..."
        ):
            try:
                result = calculate_compatibility(
                    user_profile, profile
                )
                score = result.get("score", 0)

                if score >= 80:
                    score_class = "hm-score-high"
                elif score >= 60:
                    score_class = "hm-score-mid"
                else:
                    score_class = "hm-score-low"

                st.markdown(
                    f"<div style='background:#111113;"
                    f"border:1px solid #1c1c1f;"
                    f"border-radius:14px;padding:1.4rem;"
                    f"margin-top:0.8rem;'>"
                    f"<div style='display:flex;"
                    f"align-items:center;gap:1rem;"
                    f"margin-bottom:1rem;'>"
                    f"<span class='hm-score {score_class}'>"
                    f"{score}% Match</span>"
                    f"<span style='font-size:0.85rem;"
                    f"color:#71717a;font-style:italic;'>"
                    f"{result.get('summary','')}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                r1, r2 = st.columns(2)

                with r1:
                    st.markdown(
                        "<div style='font-size:0.7rem;"
                        "font-weight:500;letter-spacing:0.1em;"
                        "text-transform:uppercase;color:#3f3f46;"
                        "margin-bottom:0.5rem;'>"
                        "Why you match</div>",
                        unsafe_allow_html=True
                    )
                    for s in result.get("strengths", []):
                        st.markdown(
                            f"<div class='hm-strength'>"
                            f"{s}</div>",
                            unsafe_allow_html=True
                        )

                with r2:
                    st.markdown(
                        "<div style='font-size:0.7rem;"
                        "font-weight:500;letter-spacing:0.1em;"
                        "text-transform:uppercase;color:#3f3f46;"
                        "margin-bottom:0.5rem;'>"
                        "Suggested Roles</div>",
                        unsafe_allow_html=True
                    )
                    roles = result.get(
                        "recommended_roles", {}
                    )
                    user_name = user_profile.get(
                        "full_name", "You"
                    )
                    st.markdown(
                        f"<div style='margin-bottom:0.5rem;'>"
                        f"<span class='hm-tag'>"
                        f"{user_name}</span>"
                        f"<span style='font-size:0.82rem;"
                        f"color:#71717a;'>"
                        f"{roles.get('user','Developer')}"
                        f"</span></div>"
                        f"<div>"
                        f"<span class='hm-tag'>"
                        f"{profile['full_name']}</span>"
                        f"<span style='font-size:0.82rem;"
                        f"color:#71717a;'>"
                        f"{roles.get('candidate','Developer')}"
                        f"</span></div>",
                        unsafe_allow_html=True
                    )

                    if result.get("potential_challenges"):
                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;"
                            "letter-spacing:0.1em;"
                            "text-transform:uppercase;"
                            "color:#3f3f46;"
                            "margin:0.8rem 0 0.4rem;'>"
                            "Challenge</div>"
                            f"<div style='font-size:0.8rem;"
                            f"color:#52525b;font-style:italic;"
                            f"font-weight:300;'>"
                            f"{result['potential_challenges']}"
                            f"</div>",
                            unsafe_allow_html=True
                        )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Could not calculate: {e}")

    # ── INVITE FLOW ───────────────────────────────────
    if st.session_state.get(f"show_msg_{safe_key}"):
        st.markdown(
            "<div style='background:#111113;"
            "border:1px solid #1c1c1f;"
            "border-radius:14px;padding:1.4rem;"
            "margin-top:0.8rem;'>"
            "<div style='font-size:0.7rem;font-weight:500;"
            "letter-spacing:0.1em;text-transform:uppercase;"
            "color:#3f3f46;margin-bottom:0.5rem;'>"
            f"Invite {profile['full_name']} to your team"
            "</div>"
            "<div style='font-size:0.8rem;color:#71717a;"
            "font-style:italic;margin-bottom:1rem;"
            "font-weight:300;'>"
            "If you already have teammates, they will each "
            "receive a vote request. All must approve before "
            f"{profile['full_name'].split()[0]} joins."
            "</div>",
            unsafe_allow_html=True
        )

        send_col1, send_col2, _ = st.columns([1, 1, 2])

        with send_col1:
            if st.button(
                "Send Invite",
                key=f"send_{safe_key}",
                use_container_width=True
            ):
                from_name = user_profile.get(
                    "full_name", "A HackMate user"
                )
                with st.spinner("Sending invite..."):
                    status = propose_team_member(
                        invitee_id=profile["id"],
                        invitee_name=profile["full_name"],
                        proposed_by_id=user.id,
                        proposed_by_name=from_name
                    )

                if status == "added_directly":
                    st.success(
                        f"{profile['full_name']} added "
                        f"to your team!"
                    )
                    st.session_state[
                        f"show_msg_{safe_key}"
                    ] = False
                    st.rerun()

                elif status == "voting_started":
                    st.success(
                        f"Vote request sent to your "
                        f"teammates! All must approve "
                        f"{profile['full_name'].split()[0]}."
                    )
                    st.session_state[
                        f"show_msg_{safe_key}"
                    ] = False
                    st.rerun()

                else:
                    st.error("Could not send invite.")

        with send_col2:
            if st.button(
                "Cancel",
                key=f"cancel_{safe_key}",
                use_container_width=True
            ):
                st.session_state[
                    f"show_msg_{safe_key}"
                ] = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)