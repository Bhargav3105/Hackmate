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
if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in first.")
    st.switch_page("pages/2_login.py")


# ── GET PROFILE ───────────────────────────────────────
profile = st.session_state.get("profile", {})
user = st.session_state.get("user", {})

# Fallback name if profile not set
name = profile.get("full_name", "Builder")
skills = profile.get("skills", [])
experience = profile.get("experience_level", "Intermediate")
availability = profile.get("availability", "3-5 hrs")
goals = profile.get("goals", [])


# ── NAVBAR ────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown("### HackMate")

with col3:
    if st.button("Sign Out"):
        st.session_state.clear()
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

    if st.button("Find Teammates"):
        st.switch_page("pages/4_find_teammates.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Project Idea"):
        st.switch_page("pages/5_match_results.py")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Update My Profile"):
        st.switch_page("pages/3_profile_setup.py")

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