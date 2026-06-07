import streamlit as st
from dotenv import load_dotenv
import os, sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import check_session
from utils.styles import load_css
from utils.supabase_client import get_team_members, parse_list_field

load_dotenv()

st.set_page_config(
    page_title="Team Workspace — HackMate",
    page_icon="H",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

# ── SESSION CHECK ─────────────────────────────────────
check_session()
if "user" not in st.session_state or not st.session_state.user:
    st.switch_page("pages/2_login.py")

profile = st.session_state.get("profile", {})
name = profile.get("full_name", "You")
user = st.session_state.get("user")

# ── LOAD REAL TEAM MEMBERS ────────────────────────────
real_members = get_team_members(user.id) if user else []
member_names = [name] + [m["name"] for m in real_members]

# ── INIT CLEAN SESSION DATA ───────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "todo": [],
        "in_progress": [],
        "done": []
    }

if "messages" not in st.session_state:
    st.session_state.messages = []

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
    "<div style='margin-bottom:1.5rem;'>"
    "<div class='hm-label'>Collaboration</div>"
    "<div class='hm-title'>Team Workspace</div>"
    "</div>",
    unsafe_allow_html=True
)

# ── TEAM MEMBERS STRIP ────────────────────────────────
st.markdown(
    "<div class='hm-label' style='margin-bottom:0.6rem;'>"
    "Team Members</div>",
    unsafe_allow_html=True
)

members_html = "".join([
    f"<span style='display:inline-flex;align-items:center;"
    f"gap:6px;background:#111113;border:1px solid #1c1c1f;"
    f"border-radius:999px;padding:4px 12px 4px 6px;"
    f"margin-right:6px;margin-bottom:6px;'>"
    f"<span style='width:22px;height:22px;border-radius:50%;"
    f"background:#18181b;border:1px solid #27272a;"
    f"display:inline-flex;align-items:center;"
    f"justify-content:center;"
    f"font-family:Playfair Display,serif;"
    f"font-size:0.7rem;color:#a1a1aa;'>{m[0].upper()}</span>"
    f"<span style='font-size:0.78rem;color:#71717a;'>{m}</span>"
    f"</span>"
    for m in member_names
])

st.markdown(
    f"<div style='margin-bottom:1.5rem;'>{members_html}</div>",
    unsafe_allow_html=True
)

# ── PROGRESS BAR ──────────────────────────────────────
total = sum(len(v) for v in st.session_state.tasks.values())
done_count = len(st.session_state.tasks["done"])
progress = done_count / total if total > 0 else 0

st.markdown(
    f"<div style='display:flex;justify-content:space-between;"
    f"align-items:center;margin-bottom:0.5rem;'>"
    f"<div class='hm-label'>Project Progress</div>"
    f"<div style='font-size:0.72rem;color:#52525b;'>"
    f"{done_count} of {total} tasks complete</div>"
    f"</div>",
    unsafe_allow_html=True
)
st.progress(progress)
st.markdown(
    "<div style='height:1.5rem'></div>",
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)

# ── TWO COLUMNS ───────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# ── LEFT: TASK BOARD ──────────────────────────────────
with left:
    st.markdown(
        "<div class='hm-label'>Task Board</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='height:0.8rem'></div>",
        unsafe_allow_html=True
    )

    # ── ADD NEW TASK ──────────────────────────────────
    with st.expander("+ Add new task"):
        new_task = st.text_input(
            "Task",
            placeholder="e.g. Build the login page",
            key="new_task_input",
            label_visibility="collapsed"
        )
        assigned_to = st.selectbox(
            "Assign to",
            options=member_names,
            key="task_assignee"
        )
        if st.button("Add Task", key="add_task_btn",
                     use_container_width=True):
            if new_task.strip():
                st.session_state.tasks["todo"].append({
                    "text": new_task.strip(),
                    "assigned": assigned_to,
                    "added_by": name
                })
                st.rerun()
            else:
                st.error("Please enter a task description.")

    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    # ── TO DO ─────────────────────────────────────────
    st.markdown(
        "<div style='font-size:0.68rem;font-weight:500;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "color:#3f3f46;margin-bottom:0.6rem;'>To Do</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.tasks["todo"]:
        st.markdown(
            "<div style='font-size:0.8rem;color:#27272a;"
            "font-style:italic;padding:0.8rem 0;'>"
            "No tasks yet. Add one above.</div>",
            unsafe_allow_html=True
        )

    for i, task in enumerate(st.session_state.tasks["todo"]):
        task_text = task["text"] if isinstance(task, dict) \
            else task
        assigned = task.get("assigned", "") \
            if isinstance(task, dict) else ""

        tc1, tc2 = st.columns([5, 1])
        with tc1:
            st.markdown(
                f"<div class='hm-task hm-task-todo'>"
                f"{task_text}"
                f"<div style='font-size:0.68rem;color:#3f3f46;"
                f"margin-top:4px;letter-spacing:0.04em;'>"
                f"→ {assigned}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with tc2:
            if st.button(
                "→",
                key=f"todo_{i}",
                help="Move to In Progress"
            ):
                task_item = st.session_state\
                    .tasks["todo"].pop(i)
                st.session_state.tasks["in_progress"]\
                    .append(task_item)
                st.rerun()

    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    # ── IN PROGRESS ───────────────────────────────────
    st.markdown(
        "<div style='font-size:0.68rem;font-weight:500;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "color:#a1a1aa;margin-bottom:0.6rem;'>In Progress</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.tasks["in_progress"]:
        st.markdown(
            "<div style='font-size:0.8rem;color:#27272a;"
            "font-style:italic;padding:0.8rem 0;'>"
            "Nothing in progress yet.</div>",
            unsafe_allow_html=True
        )

    for i, task in enumerate(
        st.session_state.tasks["in_progress"]
    ):
        task_text = task["text"] if isinstance(task, dict) \
            else task
        assigned = task.get("assigned", "") \
            if isinstance(task, dict) else ""

        tc1, tc2 = st.columns([5, 1])
        with tc1:
            st.markdown(
                f"<div class='hm-task hm-task-progress'>"
                f"{task_text}"
                f"<div style='font-size:0.68rem;color:#52525b;"
                f"margin-top:4px;letter-spacing:0.04em;'>"
                f"→ {assigned}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with tc2:
            if st.button(
                "✓",
                key=f"prog_{i}",
                help="Mark as Done"
            ):
                task_item = st.session_state\
                    .tasks["in_progress"].pop(i)
                st.session_state.tasks["done"]\
                    .append(task_item)
                st.rerun()

    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    # ── DONE ──────────────────────────────────────────
    st.markdown(
        "<div style='font-size:0.68rem;font-weight:500;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "color:#27272a;margin-bottom:0.6rem;'>Done</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.tasks["done"]:
        st.markdown(
            "<div style='font-size:0.8rem;color:#27272a;"
            "font-style:italic;padding:0.8rem 0;'>"
            "No completed tasks yet.</div>",
            unsafe_allow_html=True
        )

    for task in st.session_state.tasks["done"]:
        task_text = task["text"] if isinstance(task, dict) \
            else task
        assigned = task.get("assigned", "") \
            if isinstance(task, dict) else ""
        st.markdown(
            f"<div class='hm-task hm-task-done'>"
            f"{task_text}"
            f"<div style='font-size:0.68rem;margin-top:4px;'>"
            f"→ {assigned}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

# ── RIGHT: CHAT ───────────────────────────────────────
with right:
    st.markdown(
        "<div class='hm-label'>Team Chat</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='height:0.5rem'></div>",
        unsafe_allow_html=True
    )

    # Empty state
    if not st.session_state.messages:
        st.markdown(
            "<div style='background:#111113;"
            "border:1px solid #1c1c1f;border-radius:12px;"
            "padding:2rem;text-align:center;"
            "margin-bottom:1rem;'>"
            "<div style='font-size:0.85rem;color:#3f3f46;"
            "font-style:italic;font-weight:300;'>"
            "No messages yet. Say hello to your team.</div>"
            "</div>",
            unsafe_allow_html=True
        )

    # Messages
    for msg in st.session_state.messages:
        if msg["is_me"]:
            st.markdown(
                f"<div class='hm-chat-me'>"
                f"<div class='hm-chat-sender'>"
                f"You · {msg['time']}</div>"
                f"{msg['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='hm-chat-other'>"
                f"<div class='hm-chat-sender'>"
                f"{msg['sender']} · {msg['time']}</div>"
                f"{msg['text']}</div>",
                unsafe_allow_html=True
            )

    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    # Send message
    msg_input = st.text_input(
        "Message",
        placeholder="Say something to your team...",
        key="chat_input",
        label_visibility="collapsed"
    )

    sc1, sc2 = st.columns([4, 1])
    with sc2:
        send = st.button("Send", use_container_width=True)

    if send and msg_input.strip():
        now = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({
            "sender": name,
            "text": msg_input.strip(),
            "time": now,
            "is_me": True
        })
        st.rerun()

    st.markdown(
        "<div style='height:1.5rem'></div>",
        unsafe_allow_html=True
    )

    # ── TEAM STATS ────────────────────────────────────
    st.markdown(
        "<div class='hm-label'>Team Stats</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='height:0.5rem'></div>",
        unsafe_allow_html=True
    )

    in_prog = len(st.session_state.tasks["in_progress"])

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f"<div class='hm-stat-card'>"
            f"<div class='hm-stat-card-number'>"
            f"{done_count}</div>"
            f"<div class='hm-stat-card-label'>Done</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            f"<div class='hm-stat-card'>"
            f"<div class='hm-stat-card-number'>"
            f"{in_prog}</div>"
            f"<div class='hm-stat-card-label'>Active</div>"
            f"</div>",
            unsafe_allow_html=True
        )
    with s3:
        st.markdown(
            f"<div class='hm-stat-card'>"
            f"<div class='hm-stat-card-number'>"
            f"{len(member_names)}</div>"
            f"<div class='hm-stat-card-label'>Members</div>"
            f"</div>",
            unsafe_allow_html=True
        )