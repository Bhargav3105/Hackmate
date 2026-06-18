import streamlit as st
from dotenv import load_dotenv
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ai_helper import generate_project_ideas
from utils.auth import check_session
from utils.supabase_client import parse_list_field
from utils.styles import load_css
from utils.pdf_export import generate_project_plan_pdf

load_dotenv()

st.set_page_config(
    page_title="AI Ideas — HackMate",
    page_icon="H",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

# ── SESSION CHECK ─────────────────────────────────────
check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")

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
    "<div class='hm-title'>Project Idea Generator</div>"
    "<div style='font-size:0.85rem; color:#52525b;"
    "margin-top:0.5rem; font-weight:300;'>"
    "Tell us your stack — we generate winning buildathon ideas."
    "</div></div>",
    unsafe_allow_html=True
)

# ── OPTIONS LISTS ─────────────────────────────────────
all_skills = [
    "Python", "JavaScript", "React", "Node.js",
    "Flutter", "Machine Learning", "UI/UX Design",
    "DevOps", "Blockchain", "Data Science",
    "Django", "FastAPI", "Next.js", "SQL",
    "TensorFlow", "AWS", "Docker"
]

all_goals = [
    "Win prizes",
    "Learn new technologies",
    "Network with developers",
    "Build my portfolio",
    "Launch a startup",
    "Have fun and experiment"
]

# ── SAFE DEFAULTS ─────────────────────────────────────
saved_profile = st.session_state.get("profile", {})

safe_skills = [
    s for s in parse_list_field(saved_profile.get("skills", []))
    if s in all_skills
]

safe_goals = [
    g for g in parse_list_field(saved_profile.get("goals", []))
    if g in all_goals
]

# ── INPUTS ────────────────────────────────────────────
st.markdown(
    "<div class='hm-label'>Your Team Details</div>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='height:0.5rem'></div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    selected_skills = st.multiselect(
        "Team Skills",
        options=all_skills,
        default=safe_skills
    )

    experience = st.select_slider(
        "Experience Level",
        options=["Beginner", "Intermediate", "Advanced"]
    )

with col2:
    selected_goals = st.multiselect(
        "Team Goals",
        options=all_goals,
        default=safe_goals
    )

    team_size = st.slider(
        "Team Size",
        min_value=1,
        max_value=6,
        value=3
    )

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── GENERATE BUTTON ───────────────────────────────────
btn_col, _ = st.columns([1, 3])
with btn_col:
    generate = st.button(
        "Generate Ideas",
        use_container_width=True
    )

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── RESULTS ───────────────────────────────────────────
if generate:
    if not selected_skills:
        st.error("Please select at least one skill.")
    else:
        with st.spinner("AI is thinking..."):
            try:
                result = generate_project_ideas(
                    skills=selected_skills,
                    experience=experience,
                    goals=selected_goals,
                    team_size=team_size
                )

                ideas = result.get("ideas", [])

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='hm-label'>Results</div>"
                    "<div class='hm-title' "
                    "style='margin-bottom:1.5rem;'>"
                    "Your AI-Generated Ideas</div>",
                    unsafe_allow_html=True
                )

                for i, idea in enumerate(ideas):
                    difficulty = idea.get("difficulty", "Medium")

                    if difficulty == "Easy":
                        diff_color = "#34d399"
                    elif difficulty == "Hard":
                        diff_color = "#f87171"
                    else:
                        diff_color = "#a1a1aa"

                    # Idea header
                    st.markdown(
                        f"<div style='background:#111113;"
                        f"border:1px solid #1c1c1f;"
                        f"border-radius:16px; padding:1.8rem;"
                        f"margin-bottom:0.5rem;'>"
                        f"<div style='display:flex;"
                        f"justify-content:space-between;"
                        f"align-items:center;"
                        f"margin-bottom:0.5rem;'>"
                        f"<div style='font-family:Playfair Display,serif;"
                        f"font-size:1.2rem; font-weight:500;"
                        f"color:#f4f4f5;'>"
                        f"{i+1}. {idea.get('title')}</div>"
                        f"<span style='font-size:0.7rem;font-weight:500;"
                        f"letter-spacing:0.08em;color:{diff_color};"
                        f"border:1px solid {diff_color}22;"
                        f"padding:3px 12px;border-radius:999px;'>"
                        f"{difficulty}</span></div>"
                        f"<div style='font-size:0.88rem;color:#71717a;"
                        f"font-style:italic;margin-bottom:1rem;'>"
                        f"{idea.get('tagline')}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    # Download button for this idea
                    pdf_bytes = generate_project_plan_pdf(
                        idea,
                        team_name=saved_profile.get(
                            "full_name", "Your Team"
                        )
                    )
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_bytes,
                        file_name=(
                            f"{idea.get('title', 'project')}"
                            f"_plan.pdf"
                        ).replace(" ", "_"),
                        mime="application/pdf",
                        key=f"download_{i}"
                    )

                    st.markdown(
                        "<div style='height:0.5rem'></div>",
                        unsafe_allow_html=True
                    )

                    c1, c2 = st.columns(2)

                    with c1:
                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:#3f3f46;"
                            "margin-bottom:0.5rem;'>The Problem</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='font-size:0.85rem;"
                            f"color:#71717a;line-height:1.8;"
                            f"font-weight:300;margin-bottom:1rem;'>"
                            f"{idea.get('problem')}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:#3f3f46;"
                            "margin-bottom:0.5rem;'>Our Solution</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='font-size:0.85rem;"
                            f"color:#71717a;line-height:1.8;"
                            f"font-weight:300;margin-bottom:1rem;'>"
                            f"{idea.get('solution')}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:#3f3f46;"
                            "margin-bottom:0.5rem;'>Key Features</div>",
                            unsafe_allow_html=True
                        )
                        for f in idea.get("key_features", []):
                            st.markdown(
                                f"<div style='background:#18181b;"
                                f"border:1px solid #27272a;"
                                f"border-radius:8px;"
                                f"padding:0.5rem 0.9rem;"
                                f"font-size:0.82rem;color:#71717a;"
                                f"font-weight:300;"
                                f"margin-bottom:0.4rem;'>"
                                f"{f}</div>",
                                unsafe_allow_html=True
                            )

                    with c2:
                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:#3f3f46;"
                            "margin-bottom:0.5rem;'>Tech Stack</div>",
                            unsafe_allow_html=True
                        )
                        tech_html = "".join([
                            f"<span class='hm-tag'>{t}</span>"
                            for t in idea.get("tech_stack", [])
                        ])
                        st.markdown(
                            f"<div style='margin-bottom:1.2rem;'>"
                            f"{tech_html}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:#3f3f46;"
                            "margin-bottom:0.5rem;'>3-Day Timeline</div>",
                            unsafe_allow_html=True
                        )
                        timeline = idea.get("mvp_timeline", {})
                        for day, task in timeline.items():
                            day_label = day.replace("day_", "Day ")
                            st.markdown(
                                f"<div style='border-left:"
                                f"1px solid #3f3f46;"
                                f"padding-left:0.8rem;"
                                f"margin-bottom:0.7rem;"
                                f"font-size:0.82rem;'>"
                                f"<div style='font-size:0.68rem;"
                                f"color:#3f3f46;font-weight:500;"
                                f"letter-spacing:0.08em;"
                                f"text-transform:uppercase;"
                                f"margin-bottom:2px;'>"
                                f"{day_label}</div>"
                                f"<div style='color:#71717a;"
                                f"font-weight:300;'>{task}</div>"
                                f"</div>",
                                unsafe_allow_html=True
                            )

                        st.markdown(
                            "<div style='font-size:0.7rem;"
                            "font-weight:500;letter-spacing:0.1em;"
                            "text-transform:uppercase;color:#3f3f46;"
                            "margin-bottom:0.5rem;margin-top:0.5rem;'>"
                            "Wow Factor</div>",
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f"<div style='background:#18181b;"
                            f"border:1px solid #27272a;"
                            f"border-radius:10px;"
                            f"padding:0.8rem 1rem;"
                            f"font-size:0.82rem;color:#a1a1aa;"
                            f"font-style:italic;font-weight:300;'>"
                            f"{idea.get('wow_factor')}</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown("<hr>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Generation failed: {e}")
                st.info(
                    "Make sure your GROQ_API_KEY "
                    "is set correctly in your .env file."
                )