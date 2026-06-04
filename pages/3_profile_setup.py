import streamlit as st
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

st.set_page_config(
    page_title="Profile Setup — HackMate",
    page_icon="",
    layout="centered"
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
    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover { background: #4f46e5; }
    label { color: #9ca3af !important; }
    </style>
""", unsafe_allow_html=True)


# ── HEADER ───────────────────────────────────────────
st.markdown("""
    <div style='text-align:center; margin-bottom:1.5rem;'>
        <div style='font-size:1.6rem; font-weight:700;
             background:linear-gradient(135deg,#a78bfa,#6366f1);
             -webkit-background-clip:text;
             -webkit-text-fill-color:transparent;'>
            HackMate
        </div>
        <div style='color:#9ca3af; margin-top:0.3rem;'>
            Set up your profile so AI can find your perfect teammates
        </div>
    </div>
""", unsafe_allow_html=True)


# ── SECTION 1: BASIC INFO ─────────────────────────────
st.markdown("### Basic Info")

full_name = st.text_input(
    "Full Name",
    placeholder="e.g. Bhargav Sharma"
)

github_url = st.text_input(
    "GitHub Profile URL",
    placeholder="https://github.com/yourusername"
)

bio = st.text_area(
    "Short Bio",
    placeholder="e.g. Full-stack dev who loves building AI tools",
    max_chars=200,
    height=80
)

st.markdown("<br>", unsafe_allow_html=True)


# ── SECTION 2: SKILLS ─────────────────────────────────
st.markdown("### Skills")
st.markdown(
    "<small style='color:#6b7280'>Select all that apply</small>",
    unsafe_allow_html=True
)

all_skills = [
    "Python", "JavaScript", "React", "Node.js",
    "Flutter", "Machine Learning", "UI/UX Design",
    "DevOps", "Blockchain", "Data Science",
    "Django", "FastAPI", "Next.js", "SQL"
]

# Show skills as checkboxes in 3 columns
selected_skills = []
cols = st.columns(3)
for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        if st.checkbox(skill, key=f"skill_{skill}"):
            selected_skills.append(skill)

st.markdown("<br>", unsafe_allow_html=True)


# ── SECTION 3: EXPERIENCE ─────────────────────────────
st.markdown("### Experience Level")

experience = st.radio(
    "How would you describe yourself?",
    options=["Beginner", "Intermediate", "Advanced"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)


# ── SECTION 4: AVAILABILITY ───────────────────────────
st.markdown("### Daily Availability")

availability = st.select_slider(
    "How many hours per day can you commit?",
    options=["1-2 hrs", "3-5 hrs", "6-8 hrs", "Full time"],
    label_visibility="collapsed"
)

st.markdown(
    f"<small style='color:#6b7280'>Selected: {availability} per day</small>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)


# ── SECTION 5: GOALS ──────────────────────────────────
st.markdown("### Buildathon Goals")
st.markdown(
    "<small style='color:#6b7280'>Select all that apply</small>",
    unsafe_allow_html=True
)

all_goals = [
    "Win prizes",
    "Learn new technologies",
    "Network with developers",
    "Build my portfolio",
    "Launch a startup",
    "Have fun and experiment"
]

selected_goals = []
gcols = st.columns(2)
for i, goal in enumerate(all_goals):
    with gcols[i % 2]:
        if st.checkbox(goal, key=f"goal_{goal}"):
            selected_goals.append(goal)

st.markdown("<br><br>", unsafe_allow_html=True)


# ── SAVE BUTTON ───────────────────────────────────────
if st.button("Save Profile and Continue"):

    # Basic validation
    if not full_name:
        st.error("Please enter your full name.")

    elif len(selected_skills) == 0:
        st.error("Please select at least one skill.")

    elif len(selected_goals) == 0:
        st.error("Please select at least one goal.")

    else:
        try:
            # Save to Supabase profiles table
            profile_data = {
                "full_name": full_name,
                "github_url": github_url,
                "bio": bio,
                "skills": selected_skills,
                "experience_level": experience,
                "availability": availability,
                "goals": selected_goals,
            }

            # For now store in session so we can use it
            st.session_state.profile = profile_data

            st.success("Profile saved! Taking you to your dashboard...")
            st.balloons()

            import time
            time.sleep(1.5)
            st.switch_page("pages/6_dashboard.py")

        except Exception as e:
            st.error(f"Something went wrong: {e}")