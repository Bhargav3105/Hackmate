import streamlit as st
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

st.set_page_config(
    page_title="Login — HackMate",
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
        padding: 0.6rem;
    }
    .stButton > button:hover { background: #4f46e5; }
    input {
        background-color: #13131a !important;
        color: white !important;
        border: 1px solid #1f1f2e !important;
        border-radius: 8px !important;
    }
    label { color: #9ca3af !important; }
    </style>
""", unsafe_allow_html=True)


# ── ALREADY LOGGED IN? ────────────────────────────────
if "user" in st.session_state and st.session_state.user:
    st.switch_page("pages/3_profile_setup.py")


# ── HEADER ───────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align:center; margin-bottom:2rem;'>
        <div style='font-size:2rem; font-weight:700;
             background:linear-gradient(135deg,#a78bfa,#6366f1);
             -webkit-background-clip:text;
             -webkit-text-fill-color:transparent;'>
            HackMate
        </div>
        <div style='color:#9ca3af; margin-top:0.4rem;'>
            Your AI-powered hackathon companion
        </div>
    </div>
""", unsafe_allow_html=True)


# ── LOGIN / SIGNUP TABS ───────────────────────────────
tab1, tab2 = st.tabs(["Sign In", "Create Account"])


# ── TAB 1: SIGN IN ────────────────────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Your password",
        key="login_password"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Sign In", key="signin_btn"):
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                # Save user to session
                # Store user and token in session
                st.session_state.user = response.user
                st.session_state.session = response.session
                st.session_state.access_token = \
                    response.session.access_token

                # Try loading existing profile
                from utils.auth import load_profile_from_db
                profile = load_profile_from_db(
                    response.user.id,
                    response.session.access_token
                )

                import time

                if profile and profile.get("full_name"):
                    st.session_state.profile = profile
                    st.success("Welcome back! Taking you to dashboard...")
                    time.sleep(1)
                    st.switch_page("pages/6_dashboard.py")
                else:
                    st.success("Signed in! Let's set up your profile...")
                    time.sleep(1)
                    st.switch_page("pages/3_profile_setup.py")

            except Exception as e:
                st.error("Invalid email or password. Please try again.")


# ── TAB 2: CREATE ACCOUNT ─────────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    new_email = st.text_input(
        "Email",
        placeholder="you@example.com",
        key="signup_email"
    )

    new_password = st.text_input(
        "Password",
        type="password",
        placeholder="Min 6 characters",
        key="signup_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Repeat your password",
        key="confirm_password"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create Account", key="signup_btn"):
        if not new_email or not new_password:
            st.error("Please fill in all fields.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")

        else:
            try:
                response = supabase.auth.sign_up({
                    "email": new_email,
                    "password": new_password
                })

                st.success("""
                    Account created! Check your email for a
                    confirmation link, then sign in.
                """)

            except Exception as e:
                st.error(f"Could not create account: {e}")


# ── FEATURES PREVIEW ──────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='border-top:1px solid #1f1f2e; padding-top:1.5rem;'>
        <div style='color:#6b7280; font-size:0.8rem;
             text-align:center; margin-bottom:1rem;'>
            What you get with HackMate
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr;
             gap:0.8rem;'>
            <div style='background:#13131a; border:1px solid #1f1f2e;
                 border-radius:10px; padding:0.8rem; font-size:0.82rem;
                 color:#9ca3af;'>
                AI teammate matching based on skills
            </div>
            <div style='background:#13131a; border:1px solid #1f1f2e;
                 border-radius:10px; padding:0.8rem; font-size:0.82rem;
                 color:#9ca3af;'>
                Project ideas for your tech stack
            </div>
            <div style='background:#13131a; border:1px solid #1f1f2e;
                 border-radius:10px; padding:0.8rem; font-size:0.82rem;
                 color:#9ca3af;'>
                Compatibility scores explained
            </div>
            <div style='background:#13131a; border:1px solid #1f1f2e;
                 border-radius:10px; padding:0.8rem; font-size:0.82rem;
                 color:#9ca3af;'>
                Team workspace and task board
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)