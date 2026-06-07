import streamlit as st
from dotenv import load_dotenv
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import check_session
from utils.styles import load_css
from utils.supabase_client import save_profile, parse_list_field

load_dotenv()

st.set_page_config(
    page_title="Edit Profile — HackMate",
    page_icon="H",
    layout="centered"
)

st.markdown(load_css(), unsafe_allow_html=True)

# ── SESSION CHECK ─────────────────────────────────────
check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")

profile = st.session_state.get("profile", {})
user = st.session_state.get("user")

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
    "<div class='hm-label'>Account</div>"
    "<div class='hm-title' style='margin-bottom:2rem;'>"
    "Edit Profile</div>",
    unsafe_allow_html=True
)

# ── LOAD CURRENT VALUES ───────────────────────────────
current_skills = parse_list_field(profile.get("skills", []))
current_goals = parse_list_field(profile.get("goals", []))

# ── BASIC INFO ────────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Basic Info</div>",
    unsafe_allow_html=True
)

full_name = st.text_input(
    "Full Name",
    value=profile.get("full_name", ""),
    placeholder="Your full name"
)

github_url = st.text_input(
    "GitHub URL",
    value=profile.get("github_url", ""),
    placeholder="https://github.com/yourusername"
)

bio = st.text_area(
    "Short Bio",
    value=profile.get("bio", ""),
    placeholder="Tell teammates about yourself",
    height=80,
    max_chars=200
)

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── SKILLS ────────────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Skills</div>",
    unsafe_allow_html=True
)

all_skills = [
    "Python", "JavaScript", "React", "Node.js",
    "Flutter", "Machine Learning", "UI/UX Design",
    "DevOps", "Blockchain", "Data Science",
    "Django", "FastAPI", "Next.js", "SQL",
    "TensorFlow", "AWS", "Docker"
]

selected_skills = []
cols = st.columns(3)
for i, skill in enumerate(all_skills):
    with cols[i % 3]:
        checked = skill in current_skills
        if st.checkbox(
            skill,
            value=checked,
            key=f"skill_{skill}"
        ):
            selected_skills.append(skill)

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── EXPERIENCE ────────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Experience Level</div>",
    unsafe_allow_html=True
)

exp_options = ["Beginner", "Intermediate", "Advanced"]
current_exp = profile.get("experience_level", "Intermediate")
exp_index = exp_options.index(current_exp) \
    if current_exp in exp_options else 1

experience = st.radio(
    "Experience",
    options=exp_options,
    index=exp_index,
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── AVAILABILITY ──────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Daily Availability</div>",
    unsafe_allow_html=True
)

avail_options = ["1-2 hrs", "3-5 hrs", "6-8 hrs", "Full time"]
current_avail = profile.get("availability", "3-5 hrs")
avail_index = avail_options.index(current_avail) \
    if current_avail in avail_options else 1

availability = st.select_slider(
    "Availability",
    options=avail_options,
    value=current_avail,
    label_visibility="collapsed"
)

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── GOALS ─────────────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Buildathon Goals</div>",
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
        checked = goal in current_goals
        if st.checkbox(
            goal,
            value=checked,
            key=f"goal_{goal}"
        ):
            selected_goals.append(goal)

st.markdown(
    "<div style='height:1.5rem'></div>",
    unsafe_allow_html=True
)

# ── SAVE ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if st.button(
        "Save Changes",
        use_container_width=True
    ):
        if not full_name:
            st.error("Please enter your full name.")
        elif len(selected_skills) == 0:
            st.error("Please select at least one skill.")
        elif len(selected_goals) == 0:
            st.error("Please select at least one goal.")
        else:
            with st.spinner("Saving..."):
                updated_profile = {
                    "full_name": full_name,
                    "github_url": github_url,
                    "bio": bio,
                    "skills": selected_skills,
                    "experience_level": experience,
                    "availability": availability,
                    "goals": selected_goals,
                }

                access_token = st.session_state\
                    .get("access_token")
                result = save_profile(
                    user.id,
                    updated_profile,
                    access_token
                )

                if result:
                    st.session_state.profile = updated_profile
                    st.success("Profile updated!")
                    import time
                    time.sleep(1)
                    st.switch_page("pages/6_dashboard.py")
                else:
                    st.error("Could not save. Try again.")

with col2:
    if st.button(
        "Cancel",
        use_container_width=True
    ):
        st.switch_page("pages/6_dashboard.py")