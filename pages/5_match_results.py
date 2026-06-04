import streamlit as st
from dotenv import load_dotenv
import os
import sys

# Add parent folder to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ai_helper import generate_project_ideas, get_ai_recommendations

load_dotenv()

st.set_page_config(
    page_title="AI Ideas — HackMate",
    page_icon="",
    layout="wide"
)

# ── STYLING ──────────────────────────────────────────
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0a0a0f; color: #ffffff; }

    .idea-card {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        transition: border-color 0.2s;
    }
    .idea-card:hover { border-color: #6366f1; }

    .difficulty-badge {
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 500;
    }
    .easy { background: #064e3b; color: #6ee7b7; }
    .medium { background: #1e1b4b; color: #a78bfa; }
    .hard { background: #450a0a; color: #fca5a5; }

    .feature-item {
        background: #0d0d14;
        border: 1px solid #1f1f2e;
        border-radius: 8px;
        padding: 0.4rem 0.8rem;
        color: #9ca3af;
        font-size: 0.82rem;
        margin-bottom: 0.4rem;
    }

    .tech-tag {
        background: #1e1b4b;
        color: #a78bfa;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-right: 4px;
    }

    .timeline-item {
        border-left: 2px solid #6366f1;
        padding-left: 0.8rem;
        margin-bottom: 0.6rem;
        color: #9ca3af;
        font-size: 0.85rem;
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
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import check_session

check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")


# ── HEADER ───────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <h1 style='color:white; margin-bottom:0.3rem;'>
            AI Project Idea Generator
        </h1>
        <p style='color:#9ca3af;'>
            Tell us your stack and we generate winning buildathon ideas
        </p>
    """, unsafe_allow_html=True)
with col2:
    if st.button("Back to Dashboard"):
        st.switch_page("pages/6_dashboard.py")

st.markdown("---")


# ── INPUT SECTION ─────────────────────────────────────
st.markdown("### Your Team Details")
st.markdown(
    "<small style='color:#6b7280'>The more details you give, "
    "the better the ideas</small>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    all_skills = [
        "Python", "JavaScript", "React", "Node.js",
        "Flutter", "Machine Learning", "UI/UX Design",
        "DevOps", "Blockchain", "Data Science",
        "Django", "FastAPI", "Next.js", "SQL",
        "TensorFlow", "AWS", "Docker"
    ]

    selected_skills = st.multiselect(
        "Team Skills (select all that apply)",
        options=all_skills,
        default=st.session_state.get(
            "profile", {}
        ).get("skills", [])
    )

    experience = st.select_slider(
        "Team Experience Level",
        options=["Beginner", "Intermediate", "Advanced"]
    )

with col2:
    all_goals = [
        "Win prizes",
        "Learn new technologies",
        "Network with developers",
        "Build my portfolio",
        "Launch a startup",
        "Have fun and experiment"
    ]

    selected_goals = st.multiselect(
        "Team Goals",
        options=all_goals,
        default=st.session_state.get(
            "profile", {}
        ).get("goals", [])
    )

    team_size = st.slider(
        "Team Size",
        min_value=1,
        max_value=6,
        value=3
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── GENERATE BUTTON ───────────────────────────────────
generate_col, _ = st.columns([1, 2])
with generate_col:
    generate_clicked = st.button(
        "Generate Ideas with AI",
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# ── GENERATE IDEAS ────────────────────────────────────
if generate_clicked:

    if not selected_skills:
        st.error("Please select at least one skill.")

    else:
        with st.spinner("AI is generating your project ideas..."):
            try:
                result = generate_project_ideas(
                    skills=selected_skills,
                    experience=experience,
                    goals=selected_goals,
                    team_size=team_size
                )

                ideas = result.get("ideas", [])

                st.markdown("## Your AI-Generated Project Ideas")
                st.markdown(
                    "<small style='color:#6b7280'>"
                    "Based on your team's skills and goals</small>",
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)

                for i, idea in enumerate(ideas):
                    difficulty = idea.get("difficulty", "Medium")
                    diff_class = difficulty.lower()

                    st.markdown(f"""
                        <div class='idea-card'>
                            <div style='display:flex; justify-content:space-between;
                                 align-items:start; margin-bottom:0.8rem;'>
                                <div>
                                    <div style='font-size:1.2rem; font-weight:700;
                                         color:white;'>
                                        {i+1}. {idea.get("title")}
                                    </div>
                                    <div style='color:#6366f1; font-size:0.9rem;
                                         margin-top:0.2rem;'>
                                        {idea.get("tagline")}
                                    </div>
                                </div>
                                <span class='difficulty-badge {diff_class}'>
                                    {difficulty}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**The Problem**")
                        st.markdown(
                            f"<p style='color:#9ca3af; font-size:0.88rem;'>"
                            f"{idea.get('problem')}</p>",
                            unsafe_allow_html=True
                        )

                        st.markdown("**Our Solution**")
                        st.markdown(
                            f"<p style='color:#9ca3af; font-size:0.88rem;'>"
                            f"{idea.get('solution')}</p>",
                            unsafe_allow_html=True
                        )

                        st.markdown("**Key Features**")
                        for feature in idea.get("key_features", []):
                            st.markdown(
                                f"<div class='feature-item'>✦ {feature}</div>",
                                unsafe_allow_html=True
                            )

                    with col2:
                        st.markdown("**Tech Stack**")
                        tech_tags = "".join([
                            f"<span class='tech-tag'>{t}</span>"
                            for t in idea.get("tech_stack", [])
                        ])
                        st.markdown(
                            f"<div style='margin-bottom:1rem;'>"
                            f"{tech_tags}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown("**3-Day MVP Timeline**")
                        timeline = idea.get("mvp_timeline", {})
                        for day, task in timeline.items():
                            day_num = day.replace("day_", "Day ")
                            st.markdown(
                                f"<div class='timeline-item'>"
                                f"<strong style='color:white;'>{day_num}:</strong>"
                                f" {task}</div>",
                                unsafe_allow_html=True
                            )

                        st.markdown("**Wow Factor**")
                        st.markdown(
                            f"<div style='background:#0d0f1f; border:1px solid "
                            f"#6366f1; border-radius:8px; padding:0.6rem 0.8rem;"
                            f"color:#a78bfa; font-size:0.85rem;'>"
                            f"✦ {idea.get('wow_factor')}</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown("---")

            except Exception as e:
                st.error(f"AI generation failed: {e}")
                st.info(
                    "Make sure your OpenAI API key is set "
                    "correctly in your .env file."
                )