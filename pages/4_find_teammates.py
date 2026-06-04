import streamlit as st
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ai_helper import calculate_compatibility, get_ai_recommendations

load_dotenv()

st.set_page_config(
    page_title="Find Teammates — HackMate",
    page_icon="",
    layout="wide"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0a0a0f; color: #ffffff; }
    .skill-tag {
        background: #0d0d14;
        border: 1px solid #1f1f2e;
        color: #9ca3af;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-right: 4px;
        margin-bottom: 4px;
        display: inline-block;
    }
    .strength-item {
        background: #0a1628;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        color: #93c5fd;
        font-size: 0.82rem;
        margin-bottom: 0.4rem;
    }
    .role-badge {
        background: #1e1b4b;
        color: #a78bfa;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
    }
    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ── AUTH CHECK ────────────────────────────────────────
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import check_session

check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")

# ── SAMPLE PROFILES ───────────────────────────────────
sample_profiles = [
    {
        "full_name": "Arjun Mehta",
        "skills": ["Machine Learning", "Python", "TensorFlow", "FastAPI"],
        "experience_level": "Advanced",
        "availability": "Full time",
        "goals": ["Win prizes", "Launch a startup"],
        "bio": "ML engineer who loves building AI products from scratch.",
        "github_url": "https://github.com/arjunmehta"
    },
    {
        "full_name": "Priya Sharma",
        "skills": ["UI/UX Design", "Figma", "React", "JavaScript"],
        "experience_level": "Intermediate",
        "availability": "6-8 hrs",
        "goals": ["Build my portfolio", "Learn new technologies"],
        "bio": "Designer who codes. I make things look beautiful and work great.",
        "github_url": "https://github.com/priyasharma"
    },
    {
        "full_name": "Rahul Dev",
        "skills": ["Node.js", "MongoDB", "DevOps", "Docker"],
        "experience_level": "Intermediate",
        "availability": "3-5 hrs",
        "goals": ["Learn new technologies", "Network with developers"],
        "bio": "Backend developer obsessed with scalable systems.",
        "github_url": "https://github.com/rahuldev"
    },
    {
        "full_name": "Sneha Patel",
        "skills": ["Data Science", "SQL", "Python", "Tableau"],
        "experience_level": "Beginner",
        "availability": "3-5 hrs",
        "goals": ["Learn new technologies", "Build my portfolio"],
        "bio": "Data enthusiast turning raw numbers into insights.",
        "github_url": "https://github.com/snehapatel"
    },
    {
        "full_name": "Karan Singh",
        "skills": ["Flutter", "Dart", "Firebase", "UI/UX Design"],
        "experience_level": "Intermediate",
        "availability": "6-8 hrs",
        "goals": ["Win prizes", "Build my portfolio"],
        "bio": "Mobile developer building beautiful cross-platform apps.",
        "github_url": "https://github.com/karansingh"
    },
]

# ── HEADER ───────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <h1 style='color:white; margin-bottom:0.3rem;'>Find Teammates</h1>
        <p style='color:#9ca3af;'>AI calculates your compatibility with each person</p>
    """, unsafe_allow_html=True)
with col2:
    if st.button("Back to Dashboard"):
        st.switch_page("pages/6_dashboard.py")

st.markdown("---")

# ── USER PROFILE CHECK ────────────────────────────────
user_profile = st.session_state.get("profile", {})

if not user_profile:
    st.warning("Complete your profile first so AI can calculate compatibility scores.")
    if st.button("Set Up Profile"):
        st.switch_page("pages/3_profile_setup.py")
    st.stop()

# ── FILTERS ───────────────────────────────────────────
st.markdown("### Filter Candidates")
fc1, fc2 = st.columns(2)

with fc1:
    filter_exp = st.multiselect(
        "Experience Level",
        options=["Beginner", "Intermediate", "Advanced"]
    )
with fc2:
    filter_avail = st.multiselect(
        "Availability",
        options=["1-2 hrs", "3-5 hrs", "6-8 hrs", "Full time"]
    )

# Apply filters
filtered = sample_profiles
if filter_exp:
    filtered = [p for p in filtered if p["experience_level"] in filter_exp]
if filter_avail:
    filtered = [p for p in filtered if p["availability"] in filter_avail]

st.markdown(
    f"<small style='color:#6b7280'>Showing {len(filtered)} candidates</small>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# ── CANDIDATE CARDS ───────────────────────────────────
st.markdown("### Candidates")
st.markdown("<br>", unsafe_allow_html=True)

for profile in filtered:
    col1, col2 = st.columns([3, 1])

    with col1:
        # Name and experience
        st.markdown(f"""
            <div style='font-size:1.1rem; font-weight:700; color:white;'>
                {profile["full_name"]}
                <span style='color:#6b7280; font-size:0.85rem;
                     font-weight:400; margin-left:0.8rem;'>
                    {profile["experience_level"]} · {profile["availability"]}/day
                </span>
            </div>
            <div style='color:#9ca3af; font-size:0.88rem; margin:0.3rem 0 0.6rem;'>
                {profile["bio"]}
            </div>
            <div>
                {"".join([f"<span class='skill-tag'>{s}</span>" for s in profile["skills"]])}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        check = st.button(
            "Check Compatibility",
            key=f"btn_{profile['full_name'].replace(' ', '_')}",
            use_container_width=True
        )

    # ── COMPATIBILITY RESULT ──────────────────────────
    if check:
        with st.spinner(f"Calculating compatibility with {profile['full_name']}..."):
            try:
                result = calculate_compatibility(user_profile, profile)
                score = result.get("score", 0)

                # Pick color based on score
                if score >= 80:
                    color = "#6ee7b7"
                    bg = "#064e3b"
                elif score >= 60:
                    color = "#a78bfa"
                    bg = "#1e1b4b"
                else:
                    color = "#fca5a5"
                    bg = "#450a0a"

                # Score badge
                st.markdown(f"""
                    <div style='margin-top:1rem; margin-bottom:0.6rem;'>
                        <span style='background:{bg}; color:{color};
                             border-radius:999px; padding:6px 16px;
                             font-size:1.2rem; font-weight:700;'>
                            {score}% Match
                        </span>
                    </div>
                    <p style='color:#9ca3af; font-size:0.9rem;'>
                        {result.get("summary", "")}
                    </p>
                """, unsafe_allow_html=True)

                # Strengths and roles side by side
                r1, r2 = st.columns(2)

                with r1:
                    st.markdown("**Why you match**")
                    for s in result.get("strengths", []):
                        st.markdown(
                            f"<div class='strength-item'>✦ {s}</div>",
                            unsafe_allow_html=True
                        )

                with r2:
                    st.markdown("**Suggested Roles**")
                    roles = result.get("recommended_roles", {})
                    user_name = user_profile.get("full_name", "You")

                    st.markdown(f"""
                        <div style='margin-bottom:0.5rem;'>
                            <span style='color:#6b7280; font-size:0.82rem;'>
                                {user_name}:
                            </span>
                            <span class='role-badge'>
                                {roles.get("user", "Developer")}
                            </span>
                        </div>
                        <div>
                            <span style='color:#6b7280; font-size:0.82rem;'>
                                {profile["full_name"]}:
                            </span>
                            <span class='role-badge'>
                                {roles.get("candidate", "Developer")}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)

                    challenge = result.get("potential_challenges", "")
                    if challenge:
                        st.markdown("<br>**Potential Challenge**")
                        st.markdown(
                            f"<p style='color:#6b7280; font-size:0.82rem;'>"
                            f"{challenge}</p>",
                            unsafe_allow_html=True
                        )

            except Exception as e:
                st.error(f"Could not calculate compatibility: {e}")

    st.markdown("---")