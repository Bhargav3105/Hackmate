import streamlit as st

# Page configuration - always the FIRST streamlit command
st.set_page_config(
    page_title="HackMate",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark premium look
st.markdown("""
    <style>
    /* Hide default Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Main background */
    .stApp {
        background-color: #0a0a0f;
        color: #ffffff;
    }

    /* Hero heading */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.2;
        background: linear-gradient(135deg, #a78bfa, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    /* Subtitle */
    .hero-sub {
        font-size: 1.2rem;
        color: #9ca3af;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    /* Feature card */
    .feature-card {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s;
    }

    .feature-card:hover {
        border-color: #6366f1;
    }

    /* Stat number */
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #a78bfa;
    }

    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* Badge */
    .badge {
        background: #1e1b4b;
        color: #a78bfa;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1.5rem;
    }

    /* Button override */
    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        width: 100%;
    }

    .stButton > button:hover {
        background: #4f46e5;
    }
    </style>
""", unsafe_allow_html=True)


# ── NAVBAR ──────────────────────────────────────────
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown("### HackMate")

with col3:
    if st.button("Get Started"):
        st.switch_page("pages/2_login.py")


# ── HERO SECTION ─────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="badge">Sarvam AI Track — Developer Tools</div>',
            unsafe_allow_html=True)

st.markdown('<div class="hero-title">Find your perfect<br>hackathon team with AI</div>',
            unsafe_allow_html=True)

st.markdown('''<div class="hero-sub">
    HackMate uses AI to match you with compatible teammates,<br>
    generate winning project ideas, and help your team ship faster.
</div>''', unsafe_allow_html=True)

# CTA Buttons
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("Get Started Free"):
        st.switch_page("pages/2_login.py")
with col2:
    if st.button("See How It Works"):
        st.info("Scroll down to learn more!")


# ── FEATURE CARDS ────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### Everything your team needs")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('''<div class="feature-card">
        <h3>AI Team Matching</h3>
        <p style="color:#9ca3af">Get matched with teammates based on skills,
        goals, experience and availability.</p>
    </div>''', unsafe_allow_html=True)

with col2:
    st.markdown('''<div class="feature-card">
        <h3>Compatibility Score</h3>
        <p style="color:#9ca3af">See exactly why you match with a clear
        AI-generated compatibility breakdown.</p>
    </div>''', unsafe_allow_html=True)

with col3:
    st.markdown('''<div class="feature-card">
        <h3>AI Idea Generator</h3>
        <p style="color:#9ca3af">Tell us your stack and we generate
        buildathon ideas, features and an MVP roadmap.</p>
    </div>''', unsafe_allow_html=True)


# ── STATS ────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('''<div style="text-align:center">
        <div class="stat-number">500+</div>
        <div class="stat-label">Developers</div>
    </div>''', unsafe_allow_html=True)

with col2:
    st.markdown('''<div style="text-align:center">
        <div class="stat-number">120+</div>
        <div class="stat-label">Teams Formed</div>
    </div>''', unsafe_allow_html=True)

with col3:
    st.markdown('''<div style="text-align:center">
        <div class="stat-number">92%</div>
        <div class="stat-label">Match Accuracy</div>
    </div>''', unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''<div style="text-align:center; color:#4b5563; font-size:0.85rem;">
    Built for Sarvam AI Buildathon · HackMate © 2025
</div>''', unsafe_allow_html=True)