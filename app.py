import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.styles import load_css

st.set_page_config(
    page_title="HackMate",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(load_css(), unsafe_allow_html=True)

# Domitur-inspired animation styles + scroll reveal
st.markdown("""
<style>
@keyframes revealUp {
    0%   { opacity: 0; transform: translateY(40px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes revealFade {
    0%   { opacity: 0; }
    100% { opacity: 1; }
}
@keyframes lineGrow {
    0%   { width: 0; }
    100% { width: 100%; }
}
@keyframes counterUp {
    0%   { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

.reveal-1 { animation: revealUp 0.9s cubic-bezier(0.16,1,0.3,1) 0.1s both; }
.reveal-2 { animation: revealUp 0.9s cubic-bezier(0.16,1,0.3,1) 0.25s both; }
.reveal-3 { animation: revealUp 0.9s cubic-bezier(0.16,1,0.3,1) 0.4s both; }
.reveal-4 { animation: revealUp 0.9s cubic-bezier(0.16,1,0.3,1) 0.55s both; }
.reveal-fade { animation: revealFade 1.2s ease 0.2s both; }

.stat-reveal-1 { animation: counterUp 0.8s cubic-bezier(0.16,1,0.3,1) 0.3s both; }
.stat-reveal-2 { animation: counterUp 0.8s cubic-bezier(0.16,1,0.3,1) 0.45s both; }
.stat-reveal-3 { animation: counterUp 0.8s cubic-bezier(0.16,1,0.3,1) 0.6s both; }
.stat-reveal-4 { animation: counterUp 0.8s cubic-bezier(0.16,1,0.3,1) 0.75s both; }

.feature-hover {
    padding: 1.8rem 0;
    border-top: 1px solid #1c1c1f;
    transition: padding-left 0.4s cubic-bezier(0.16,1,0.3,1),
                border-color 0.3s ease;
    cursor: default;
}
.feature-hover:hover {
    padding-left: 1rem;
    border-top-color: #52525b;
}

.nav-line {
    height: 1px;
    background: #1c1c1f;
    margin: 1.5rem 0;
    animation: lineGrow 1s cubic-bezier(0.16,1,0.3,1) 0.5s both;
}

.hero-eyebrow {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #52525b;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 500;
    line-height: 1.08;
    color: #f4f4f5;
    letter-spacing: -0.025em;
    margin-bottom: 1.8rem;
}

.hero-body {
    font-size: 0.95rem;
    font-weight: 300;
    color: #71717a;
    line-height: 1.9;
    max-width: 420px;
    margin-bottom: 2.5rem;
}

.stat-item {
    padding: 2.5rem 1.5rem;
    text-align: center;
}

.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 500;
    color: #f4f4f5;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.stat-lbl {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3f3f46;
}

.section-eyebrow {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3f3f46;
    margin-bottom: 0.8rem;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 500;
    color: #f4f4f5;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.section-body {
    font-size: 0.85rem;
    color: #52525b;
    line-height: 1.9;
    font-weight: 300;
    max-width: 320px;
}

.feat-num {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: #3f3f46;
    margin-bottom: 0.7rem;
}

.feat-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 500;
    color: #f4f4f5;
    margin-bottom: 0.5rem;
}

.feat-desc {
    font-size: 0.82rem;
    color: #52525b;
    line-height: 1.8;
    font-weight: 300;
}

.cta-wrap {
    padding: 6rem 0;
    text-align: center;
    border-top: 1px solid #1c1c1f;
    border-bottom: 1px solid #1c1c1f;
}

.cta-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 500;
    color: #f4f4f5;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}

.cta-sub {
    font-size: 0.88rem;
    color: #52525b;
    font-weight: 300;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────
st.markdown(
    "<div style='height:48px'></div>",
    unsafe_allow_html=True
)

n1, n2, n3 = st.columns([1, 5, 1])
with n1:
    st.markdown(
        "<div class='hm-logo reveal-fade'>HackMate</div>",
        unsafe_allow_html=True
    )
with n3:
    if st.button("Sign in"):
        st.switch_page("pages/2_login.py")

st.markdown(
    "<div class='nav-line'></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='height:60px'></div>",
    unsafe_allow_html=True
)

# ── HERO ──────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown(
        "<div class='hero-eyebrow reveal-1'>"
        "Sarvam AI · Developer Tools Track"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='hero-title reveal-2'>"
        "The intelligent way<br>to build your<br>"
        "hackathon team."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='hero-body reveal-3'>"
        "HackMate uses AI to match you with the right teammates, "
        "generate project ideas tailored to your skills, "
        "and help your team ship something great."
        "</div>",
        unsafe_allow_html=True
    )
    b1, b2, b3 = st.columns([1, 1, 3])
    with b1:
        if st.button("Get started"):
            st.switch_page("pages/2_login.py")

with col2:
    # Elegant floating preview card
    st.markdown("""
        <div class='reveal-4' style='
            background:#111113;
            border:1px solid #1c1c1f;
            border-radius:20px;
            padding:2rem;
            margin-top:2rem;
            animation: revealUp 1s cubic-bezier(0.16,1,0.3,1) 0.6s both;
        '>
            <div style='font-size:0.65rem; font-weight:500;
                 letter-spacing:0.12em; text-transform:uppercase;
                 color:#3f3f46; margin-bottom:1.5rem;'>
                AI Match Preview
            </div>
            <div style='
                display:flex; align-items:center;
                gap:1rem; padding:1rem 0;
                border-bottom:1px solid #1c1c1f;
                animation:revealUp 0.7s cubic-bezier(0.16,1,0.3,1) 0.8s both;
            '>
                <div style='width:38px;height:38px;border-radius:10px;
                     background:#18181b;border:1px solid #27272a;
                     display:flex;align-items:center;justify-content:center;
                     font-family:Playfair Display,serif;color:#71717a;
                     font-size:0.9rem;flex-shrink:0;'>A</div>
                <div style='flex:1;'>
                    <div style='font-family:Playfair Display,serif;
                         font-size:0.92rem;color:#f4f4f5;
                         margin-bottom:2px;'>Arjun Mehta</div>
                    <div style='font-size:0.72rem;color:#52525b;'>
                        ML Engineer · Full time</div>
                </div>
                <span style='font-size:0.75rem;font-weight:600;
                     padding:3px 10px;border-radius:999px;
                     background:rgba(16,185,129,0.08);
                     color:#34d399;
                     border:1px solid rgba(16,185,129,0.15);'>
                    92%
                </span>
            </div>
            <div style='
                display:flex; align-items:center;
                gap:1rem; padding:1rem 0;
                border-bottom:1px solid #1c1c1f;
                animation:revealUp 0.7s cubic-bezier(0.16,1,0.3,1) 0.95s both;
            '>
                <div style='width:38px;height:38px;border-radius:10px;
                     background:#18181b;border:1px solid #27272a;
                     display:flex;align-items:center;justify-content:center;
                     font-family:Playfair Display,serif;color:#71717a;
                     font-size:0.9rem;flex-shrink:0;'>P</div>
                <div style='flex:1;'>
                    <div style='font-family:Playfair Display,serif;
                         font-size:0.92rem;color:#f4f4f5;
                         margin-bottom:2px;'>Priya Sharma</div>
                    <div style='font-size:0.72rem;color:#52525b;'>
                        UI/UX Designer · 6-8 hrs</div>
                </div>
                <span style='font-size:0.75rem;font-weight:600;
                     padding:3px 10px;border-radius:999px;
                     background:rgba(161,161,170,0.08);
                     color:#a1a1aa;
                     border:1px solid rgba(161,161,170,0.12);'>
                    87%
                </span>
            </div>
            <div style='
                display:flex; align-items:center;
                gap:1rem; padding:1rem 0;
                animation:revealUp 0.7s cubic-bezier(0.16,1,0.3,1) 1.1s both;
            '>
                <div style='width:38px;height:38px;border-radius:10px;
                     background:#18181b;border:1px solid #27272a;
                     display:flex;align-items:center;justify-content:center;
                     font-family:Playfair Display,serif;color:#71717a;
                     font-size:0.9rem;flex-shrink:0;'>R</div>
                <div style='flex:1;'>
                    <div style='font-family:Playfair Display,serif;
                         font-size:0.92rem;color:#f4f4f5;
                         margin-bottom:2px;'>Rahul Dev</div>
                    <div style='font-size:0.72rem;color:#52525b;'>
                        Backend Dev · 3-5 hrs</div>
                </div>
                <span style='font-size:0.75rem;font-weight:600;
                     padding:3px 10px;border-radius:999px;
                     background:rgba(161,161,170,0.08);
                     color:#a1a1aa;
                     border:1px solid rgba(161,161,170,0.12);'>
                    81%
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<div style='height:100px'></div>",
    unsafe_allow_html=True
)

# ── STATS BAR ─────────────────────────────────────────
stats = [
    ("500+", "Developers", "stat-reveal-1"),
    ("120+", "Teams Formed", "stat-reveal-2"),
    ("92%",  "Match Accuracy", "stat-reveal-3"),
    ("3 min","To Find a Team", "stat-reveal-4"),
]

stats_html = (
    "<div style='border-top:1px solid #1c1c1f;"
    "border-bottom:1px solid #1c1c1f;'>"
    "<div style='display:grid;"
    "grid-template-columns:1fr 1fr 1fr 1fr;'>"
)

for i, (num, label, cls) in enumerate(stats):
    br = "border-right:1px solid #1c1c1f;" if i < 3 else ""
    stats_html += (
        f"<div class='stat-item {cls}' style='{br}'>"
        f"<div class='stat-num'>{num}</div>"
        f"<div class='stat-lbl'>{label}</div>"
        f"</div>"
    )

stats_html += "</div></div>"
st.markdown(stats_html, unsafe_allow_html=True)

st.markdown(
    "<div style='height:100px'></div>",
    unsafe_allow_html=True
)

# ── FEATURES ──────────────────────────────────────────
f1, spacer, f2 = st.columns([1, 0.1, 2])

with f1:
    st.markdown(
        "<div class='section-eyebrow reveal-1'>What it does</div>"
        "<div class='section-heading reveal-2'>"
        "Built for<br>serious<br>builders.</div>"
        "<div class='section-body reveal-3'>"
        "Every feature in HackMate is designed to help you "
        "form a stronger team and ship faster."
        "</div>",
        unsafe_allow_html=True
    )

with f2:
    features = [
        ("01", "AI Team Matching",
         "Matched by skills, goals, experience and availability. "
         "No more random teaming or cold messages."),
        ("02", "Compatibility Score",
         "A clear AI-generated score that explains exactly "
         "why two people work well together."),
        ("03", "Project Idea Generator",
         "Tell us your stack. Get three detailed ideas "
         "with features, tech and a 3-day MVP plan."),
        ("04", "Team Workspace",
         "Tasks, progress tracking and chat — "
         "everything your team needs in one place."),
    ]

    for num, title, desc in features:
        st.markdown(
            f"<div class='feature-hover'>"
            f"<div class='feat-num'>{num}</div>"
            f"<div class='feat-title'>{title}</div>"
            f"<div class='feat-desc'>{desc}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

st.markdown(
    "<div style='height:100px'></div>",
    unsafe_allow_html=True
)

# ── CTA ───────────────────────────────────────────────
st.markdown(
    "<div class='cta-wrap reveal-1'>"
    "<div style='font-size:0.65rem;font-weight:500;"
    "letter-spacing:0.15em;text-transform:uppercase;"
    "color:#3f3f46;margin-bottom:1.5rem;'>Free to use</div>"
    "<div class='cta-title'>Ready to find<br>your team?</div>"
    "<div class='cta-sub'>"
    "Join hundreds of developers already using HackMate."
    "</div>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='height:12px'></div>",
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns([2, 1, 2])
with c2:
    if st.button("Get started", use_container_width=True,
                 key="cta_btn"):
        st.switch_page("pages/2_login.py")

st.markdown(
    "<div style='height:60px'></div>",
    unsafe_allow_html=True
)

# ── FOOTER ────────────────────────────────────────────
st.markdown(
    "<div style='border-top:1px solid #1c1c1f;"
    "padding:2rem 0;"
    "display:flex;justify-content:space-between;"
    "align-items:center;'>"
    "<div class='hm-logo'>HackMate</div>"
    "<div style='font-size:0.7rem;color:#27272a;"
    "letter-spacing:0.06em;'>"
    "Sarvam AI Buildathon · 2025</div>"
    "</div>",
    unsafe_allow_html=True
)