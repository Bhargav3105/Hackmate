import streamlit as st
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import check_session

load_dotenv()

st.set_page_config(
    page_title="Team Workspace — HackMate",
    page_icon="",
    layout="wide"
)

# ── SESSION CHECK ─────────────────────────────────────
check_session()

if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")

# ── STYLING ──────────────────────────────────────────
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0a0a0f; color: #ffffff; }

    .task-card {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
    }
    .task-todo { border-left: 3px solid #6366f1; }
    .task-progress { border-left: 3px solid #f59e0b; }
    .task-done { border-left: 3px solid #10b981; }

    .chat-bubble-me {
        background: #1e1b4b;
        border-radius: 12px 12px 4px 12px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.6rem;
        margin-left: 20%;
        color: #e0e7ff;
        font-size: 0.88rem;
    }
    .chat-bubble-other {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 12px 12px 12px 4px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.6rem;
        margin-right: 20%;
        color: #9ca3af;
        font-size: 0.88rem;
    }
    .member-chip {
        background: #13131a;
        border: 1px solid #1f1f2e;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.82rem;
        color: #9ca3af;
        display: inline-block;
        margin-right: 6px;
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

# ── INIT SESSION DATA ─────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "todo": [
            "Set up project repository",
            "Design database schema",
            "Create landing page wireframe"
        ],
        "in_progress": [
            "Build authentication system",
            "Implement AI matching algorithm"
        ],
        "done": [
            "Project idea finalised",
            "Team formed"
        ]
    }

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "sender": "Arjun Mehta",
            "text": "Hey team! Ready to start building?",
            "time": "10:30 AM",
            "is_me": False
        },
        {
            "sender": "Priya Sharma",
            "text": "Yes! I have the designs ready. Sharing them now.",
            "time": "10:32 AM",
            "is_me": False
        },
    ]

# ── HEADER ───────────────────────────────────────────
profile = st.session_state.get("profile", {})
name = profile.get("full_name", "Builder")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <h1 style='color:white; margin-bottom:0.2rem;'>
            Team Workspace
        </h1>
        <p style='color:#9ca3af;'>
            Collaborate, track tasks and ship together
        </p>
    """, unsafe_allow_html=True)
with col2:
    if st.button("Back to Dashboard"):
        st.switch_page("pages/6_dashboard.py")

st.markdown("---")

# ── TEAM MEMBERS ─────────────────────────────────────
st.markdown("**Team Members**")
members = [name, "Arjun Mehta", "Priya Sharma"]
member_html = "".join([
    f"<span class='member-chip'>{m}</span>"
    for m in members
])
st.markdown(member_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── TWO COLUMN LAYOUT ─────────────────────────────────
left, right = st.columns([1, 1])

# ── LEFT: TASK BOARD ──────────────────────────────────
with left:
    st.markdown("### Task Board")
    st.markdown("<br>", unsafe_allow_html=True)

    # Add new task
    with st.expander("+ Add New Task"):
        new_task = st.text_input(
            "Task description",
            placeholder="e.g. Build the login page",
            key="new_task_input"
        )
        task_col1, task_col2 = st.columns(2)
        with task_col1:
            task_status = st.selectbox(
                "Status",
                options=["todo", "in_progress", "done"],
                key="task_status"
            )
        with task_col2:
            if st.button("Add Task", key="add_task_btn"):
                if new_task:
                    st.session_state.tasks[task_status].append(new_task)
                    st.success("Task added!")
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # TO DO
    st.markdown(
        "<div style='color:#6366f1; font-weight:600; "
        "margin-bottom:0.5rem;'>TO DO</div>",
        unsafe_allow_html=True
    )
    for i, task in enumerate(st.session_state.tasks["todo"]):
        tc1, tc2 = st.columns([4, 1])
        with tc1:
            st.markdown(
                f"<div class='task-card task-todo'>{task}</div>",
                unsafe_allow_html=True
            )
        with tc2:
            if st.button("→", key=f"todo_{i}", help="Move to In Progress"):
                st.session_state.tasks["todo"].remove(task)
                st.session_state.tasks["in_progress"].append(task)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # IN PROGRESS
    st.markdown(
        "<div style='color:#f59e0b; font-weight:600; "
        "margin-bottom:0.5rem;'>IN PROGRESS</div>",
        unsafe_allow_html=True
    )
    for i, task in enumerate(st.session_state.tasks["in_progress"]):
        tc1, tc2 = st.columns([4, 1])
        with tc1:
            st.markdown(
                f"<div class='task-card task-progress'>{task}</div>",
                unsafe_allow_html=True
            )
        with tc2:
            if st.button("✓", key=f"prog_{i}", help="Mark as Done"):
                st.session_state.tasks["in_progress"].remove(task)
                st.session_state.tasks["done"].append(task)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # DONE
    st.markdown(
        "<div style='color:#10b981; font-weight:600; "
        "margin-bottom:0.5rem;'>DONE</div>",
        unsafe_allow_html=True
    )
    for task in st.session_state.tasks["done"]:
        st.markdown(
            f"<div class='task-card task-done' style='opacity:0.7;'>"
            f"<s>{task}</s></div>",
            unsafe_allow_html=True
        )

    # Progress
    total = sum(len(v) for v in st.session_state.tasks.values())
    done = len(st.session_state.tasks["done"])
    progress = done / total if total > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<small style='color:#6b7280'>"
        f"Progress: {done}/{total} tasks complete</small>",
        unsafe_allow_html=True
    )
    st.progress(progress)

# ── RIGHT: TEAM CHAT ──────────────────────────────────
with right:
    st.markdown("### Team Chat")
    st.markdown("<br>", unsafe_allow_html=True)

    # Display messages
    for msg in st.session_state.messages:
        if msg["is_me"]:
            st.markdown(f"""
                <div class='chat-bubble-me'>
                    <div style='font-size:0.75rem;
                         color:#818cf8; margin-bottom:3px;'>
                        You · {msg["time"]}
                    </div>
                    {msg["text"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='chat-bubble-other'>
                    <div style='font-size:0.75rem;
                         color:#6b7280; margin-bottom:3px;'>
                        {msg["sender"]} · {msg["time"]}
                    </div>
                    {msg["text"]}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Send message
    msg_input = st.text_input(
        "Type a message",
        placeholder="Say something to your team...",
        key="chat_input",
        label_visibility="collapsed"
    )

    send_col1, send_col2 = st.columns([3, 1])
    with send_col2:
        send = st.button("Send", use_container_width=True)

    if send and msg_input:
        now = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({
            "sender": name,
            "text": msg_input,
            "time": now,
            "is_me": True
        })
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Team stats
    st.markdown("### Team Stats")
    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"""
            <div style='background:#13131a; border:1px solid #1f1f2e;
                 border-radius:10px; padding:1rem; text-align:center;'>
                <div style='font-size:1.8rem; font-weight:700;
                     color:#a78bfa;'>{done}</div>
                <div style='color:#6b7280; font-size:0.82rem;'>
                    Tasks Done
                </div>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
            <div style='background:#13131a; border:1px solid #1f1f2e;
                 border-radius:10px; padding:1rem; text-align:center;'>
                <div style='font-size:1.8rem; font-weight:700;
                     color:#a78bfa;'>{len(members)}</div>
                <div style='color:#6b7280; font-size:0.82rem;'>
                    Team Members
                </div>
            </div>
        """, unsafe_allow_html=True)