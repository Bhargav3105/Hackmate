import streamlit as st
from dotenv import load_dotenv
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from supabase import create_client
from utils.styles import load_css

st.set_page_config(
    page_title="Sign in — HackMate",
    page_icon="H",
    layout="centered"
)

st.markdown(load_css(), unsafe_allow_html=True)
st.markdown("""
    <style>
    .block-container {
        max-width: 400px !important;
        padding-top: 5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

if st.session_state.get("user") and \
   st.session_state.get("profile", {}).get("full_name"):
    st.switch_page("pages/6_dashboard.py")

# ── LOGO ──────────────────────────────────────────────
st.markdown(
    "<div class='anim-1' style='text-align:center;"
    "margin-bottom:3rem;'>"
    "<div class='hm-logo' style='font-size:1.6rem;"
    "margin-bottom:0.6rem;'>HackMate</div>"
    "<div style='font-size:0.8rem; color:#52525b;"
    "font-weight:300; letter-spacing:0.02em;'>"
    "Sign in to continue building</div>"
    "</div>",
    unsafe_allow_html=True
)

# ── TABS ──────────────────────────────────────────────
tab1, tab2 = st.tabs(["Sign in", "Create account"])

with tab1:
    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        key="login_email"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Your password",
        key="login_password"
    )

    st.markdown(
        "<div style='height:0.6rem'></div>",
        unsafe_allow_html=True
    )

    if st.button("Continue", key="signin_btn",
                 use_container_width=True):
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                st.session_state.user = response.user
                st.session_state.session = response.session
                st.session_state.access_token = \
                    response.session.access_token

                from utils.auth import load_profile_from_db
                profile = load_profile_from_db(response.user.id)

                import time
                if profile and profile.get("full_name"):
                    st.session_state.profile = profile
                    st.success("Welcome back.")
                    time.sleep(0.8)
                    st.switch_page("pages/6_dashboard.py")
                else:
                    st.success("Signed in.")
                    time.sleep(0.8)
                    st.switch_page("pages/3_profile_setup.py")

            except Exception:
                st.error("Incorrect email or password.")

with tab2:
    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    new_email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        key="signup_email"
    )
    new_password = st.text_input(
        "Password",
        type="password",
        placeholder="Min 6 characters",
        key="signup_password"
    )
    confirm = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Repeat password",
        key="confirm_password"
    )

    st.markdown(
        "<div style='height:0.6rem'></div>",
        unsafe_allow_html=True
    )

    if st.button("Create account", key="signup_btn",
                 use_container_width=True):
        if not new_email or not new_password:
            st.error("Please fill in all fields.")
        elif new_password != confirm:
            st.error("Passwords do not match.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            try:
                supabase.auth.sign_up({
                    "email": new_email,
                    "password": new_password
                })
                st.success(
                    "Account created. Check your email "
                    "to confirm, then sign in."
                )
            except Exception as e:
                st.error(f"Could not create account: {e}")

# ── BOTTOM NOTE ───────────────────────────────────────
st.markdown(
    "<div style='text-align:center; margin-top:2rem;"
    "color:#3f3f46; font-size:0.72rem; font-weight:300;'>"
    "By continuing you agree to our terms of service."
    "</div>",
    unsafe_allow_html=True
)