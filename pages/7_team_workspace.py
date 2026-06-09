import streamlit as st
from dotenv import load_dotenv
import os, sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
)))
from utils.auth import check_session
from utils.styles import load_css
from utils.supabase_client import (
    get_team_members,
    get_pending_votes_for_user,
    cast_vote,
    parse_list_field,
    send_team_message,
    get_team_messages,
    add_team_task,
    get_team_tasks,
    update_task_status,
    delete_team_task
)
from utils.ai_helper import assign_team_roles
load_dotenv()

st.set_page_config(
    page_title="Team Workspace — HackMate",
    page_icon="H",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

# ── SESSION CHECK ─────────────────────────────────────
check_session()
if "user" not in st.session_state or \
        not st.session_state.user:
    st.switch_page("pages/2_login.py")

profile = st.session_state.get("profile", {})
name = profile.get("full_name", "You")
user = st.session_state.get("user")

# ── LOAD REAL TEAM MEMBERS ────────────────────────────
real_members = get_team_members(user.id) if user else []
member_names = [name] + [m["name"] for m in real_members]
team_ids = [m["id"] for m in real_members]

# ── LOAD TASKS FROM DATABASE ──────────────────────────
all_tasks = get_team_tasks(user.id) if user else []
todo_tasks = [t for t in all_tasks
              if t["status"] == "todo"]
progress_tasks = [t for t in all_tasks
                  if t["status"] == "in_progress"]
done_tasks = [t for t in all_tasks
              if t["status"] == "done"]

total = len(all_tasks)
done_count = len(done_tasks)
in_prog = len(progress_tasks)
progress = done_count / total if total > 0 else 0

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
    f"<span style='display:inline-flex;"
    f"align-items:center;gap:6px;"
    f"background:#111113;border:1px solid #1c1c1f;"
    f"border-radius:999px;"
    f"padding:4px 12px 4px 6px;"
    f"margin-right:6px;margin-bottom:6px;'>"
    f"<span style='width:22px;height:22px;"
    f"border-radius:50%;background:#18181b;"
    f"border:1px solid #27272a;"
    f"display:inline-flex;align-items:center;"
    f"justify-content:center;"
    f"font-family:Playfair Display,serif;"
    f"font-size:0.7rem;color:#a1a1aa;'>"
    f"{m[0].upper()}</span>"
    f"<span style='font-size:0.78rem;color:#71717a;'>"
    f"{m}</span></span>"
    for m in member_names
])

st.markdown(
    f"<div style='margin-bottom:1.5rem;'>"
    f"{members_html}</div>",
    unsafe_allow_html=True
)

# ── INVITE BUTTON ─────────────────────────────────────
if st.button("Find and Invite Teammates →"):
    st.switch_page("pages/4_find_teammates.py")

st.markdown(
    "<div style='font-size:0.78rem;color:#3f3f46;"
    "font-weight:300;margin-top:0.4rem;"
    "margin-bottom:1.5rem;'>"
    "Browse real profiles and invite compatible "
    "teammates.</div>",
    unsafe_allow_html=True
)

# ── PENDING TEAM VOTES ────────────────────────────────
pending_votes = get_pending_votes_for_user(user.id) \
    if user else []

if pending_votes:
    st.markdown(
        "<div class='hm-label' "
        "style='margin-bottom:0.8rem;'>"
        "Team Vote Requests</div>",
        unsafe_allow_html=True
    )

    for vote in pending_votes:
        inv = vote.get("team_invitations", {})
        if not inv:
            continue

        invitee_name = inv.get("invitee_name", "Someone")
        proposed_by = inv.get("proposer_name", "A teammate")
        invitation_id = vote.get("invitation_id")
        vote_id = vote.get("id")
        invitee_id = inv.get("invitee_id")

        st.markdown(
            f"<div style='background:#111113;"
            f"border:1px solid #27272a;"
            f"border-radius:14px;padding:1.2rem 1.4rem;"
            f"margin-bottom:0.8rem;'>"
            f"<div style='font-size:0.68rem;font-weight:500;"
            f"letter-spacing:0.1em;text-transform:uppercase;"
            f"color:#3f3f46;margin-bottom:0.5rem;'>"
            f"Team Vote Required</div>"
            f"<div style='font-family:Playfair Display,serif;"
            f"font-size:0.95rem;color:#f4f4f5;"
            f"margin-bottom:0.3rem;'>"
            f"{proposed_by} wants to add "
            f"{invitee_name}</div>"
            f"<div style='font-size:0.78rem;color:#71717a;"
            f"font-style:italic;font-weight:300;'>"
            f"{invitee_name} accepted the invite. "
            f"Your vote determines if they join."
            f"</div></div>",
            unsafe_allow_html=True
        )

        vc1, vc2, vc3 = st.columns([2, 1, 1])

        with vc2:
            if st.button(
                "Approve",
                key=f"ws_approve_{vote_id}",
                use_container_width=True
            ):
                result = cast_vote(
                    vote_id=vote_id,
                    invitation_id=invitation_id,
                    vote_value="accepted",
                    voter_id=user.id,
                    voter_name=name,
                    invitee_id=invitee_id,
                    invitee_name=invitee_name
                )
                if result == "approved":
                    st.success(
                        f"{invitee_name} joined "
                        f"your team!"
                    )
                else:
                    st.success(
                        "Vote recorded. Waiting "
                        "for other teammates."
                    )
                st.rerun()

        with vc3:
            if st.button(
                "Reject",
                key=f"ws_reject_{vote_id}",
                use_container_width=True
            ):
                cast_vote(
                    vote_id=vote_id,
                    invitation_id=invitation_id,
                    vote_value="rejected",
                    voter_id=user.id,
                    voter_name=name,
                    invitee_id=invitee_id,
                    invitee_name=invitee_name
                )
                st.info(f"{invitee_name} was not added.")
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

# ── AI ROLE ASSIGNMENT ────────────────────────────────
st.markdown(
    "<div class='hm-label' style='margin-bottom:0.6rem;'>"
    "AI Role Assignment</div>",
    unsafe_allow_html=True
)

with st.expander("Generate AI roles for your team"):

    project_context = st.text_input(
        "Project idea (optional)",
        placeholder="e.g. AI-powered developer tool",
        key="project_context_input",
        label_visibility="collapsed"
    )

    if st.button(
        "Assign Roles with AI",
        key="assign_roles_btn",
        use_container_width=False
    ):
        if len(member_names) < 2:
            st.warning(
                "Add at least one teammate first "
                "to get role assignments."
            )
        else:
            with st.spinner(
                "AI is analysing your team..."
            ):
                try:
                    # Build team member data
                    from utils.supabase_client import \
                        get_all_profiles, get_profile

                    team_data = []

                    # Add current user
                    my_profile = st.session_state\
                        .get("profile", {})
                    team_data.append({
                        "name": name,
                        "skills": parse_list_field(
                            my_profile.get("skills", [])
                        )
                    })

                    # Add each team member
                    for member in real_members:
                        mp = get_profile(member["id"])
                        if mp:
                            team_data.append({
                                "name": member["name"],
                                "skills": parse_list_field(
                                    mp.get("skills", [])
                                )
                            })
                        else:
                            team_data.append({
                                "name": member["name"],
                                "skills": []
                            })

                    result = assign_team_roles(
                        team_members=team_data,
                        project_idea=project_context
                    )

                    roles = result.get("roles", [])
                    summary = result.get(
                        "team_summary", ""
                    )

                    # Team summary
                    st.markdown(
                        f"<div style='background:#111113;"
                        f"border:1px solid #1c1c1f;"
                        f"border-radius:12px;"
                        f"padding:1rem 1.2rem;"
                        f"margin-bottom:1rem;'>"
                        f"<div style='font-size:0.68rem;"
                        f"font-weight:500;"
                        f"letter-spacing:0.1em;"
                        f"text-transform:uppercase;"
                        f"color:#3f3f46;"
                        f"margin-bottom:0.4rem;'>"
                        f"Team Summary</div>"
                        f"<div style='font-size:0.85rem;"
                        f"color:#a1a1aa;font-style:italic;"
                        f"font-weight:300;'>"
                        f"{summary}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    # Individual roles
                    for role in roles:
                        responsibilities = "".join([
                            f"<div style='font-size:0.78rem;"
                            f"color:#71717a;font-weight:300;"
                            f"padding:3px 0;'>"
                            f"· {r}</div>"
                            for r in role.get(
                                "responsibilities", []
                            )
                        ])

                        st.markdown(
                            f"<div style='background:#111113;"
                            f"border:1px solid #1c1c1f;"
                            f"border-radius:12px;"
                            f"padding:1.2rem;"
                            f"margin-bottom:0.6rem;'>"
                            f"<div style='display:flex;"
                            f"justify-content:space-between;"
                            f"align-items:center;"
                            f"margin-bottom:0.5rem;'>"
                            f"<div style='font-family:"
                            f"Playfair Display,serif;"
                            f"font-size:0.95rem;"
                            f"color:#f4f4f5;'>"
                            f"{role.get('name')}</div>"
                            f"<span style='font-size:0.72rem;"
                            f"font-weight:500;"
                            f"letter-spacing:0.06em;"
                            f"background:#18181b;"
                            f"border:1px solid #27272a;"
                            f"color:#a1a1aa;"
                            f"padding:3px 10px;"
                            f"border-radius:999px;'>"
                            f"{role.get('role')}"
                            f"</span></div>"
                            f"<div style='font-size:0.78rem;"
                            f"color:#52525b;"
                            f"font-style:italic;"
                            f"margin-bottom:0.5rem;'>"
                            f"{role.get('why')}</div>"
                            f"{responsibilities}"
                            f"</div>",
                            unsafe_allow_html=True
                        )

                except Exception as e:
                    st.error(
                        f"Role assignment failed: {e}"
                    )

st.markdown(
    "<div style='height:1rem'></div>",
    unsafe_allow_html=True
)

# ── PROGRESS BAR ──────────────────────────────────────
st.markdown(
    f"<div style='display:flex;"
    f"justify-content:space-between;"
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
        if st.button(
            "Add Task",
            key="add_task_btn",
            use_container_width=True
        ):
            if new_task.strip():
                success = add_team_task(
                    created_by_id=user.id,
                    created_by_name=name,
                    team_member_ids=team_ids,
                    task_text=new_task.strip(),
                    assigned_to=assigned_to
                )
                if success:
                    st.rerun()
                else:
                    st.error("Could not add task.")
            else:
                st.error(
                    "Please enter a task description."
                )

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

    if not todo_tasks:
        st.markdown(
            "<div style='font-size:0.8rem;color:#27272a;"
            "font-style:italic;padding:0.8rem 0;'>"
            "No tasks yet. Add one above.</div>",
            unsafe_allow_html=True
        )

    for task in todo_tasks:
        task_id = task["id"]
        task_text = task["task_text"]
        assigned = task["assigned_to"]

        tc1, tc2, tc3 = st.columns([5, 1, 1])
        with tc1:
            st.markdown(
                f"<div class='hm-task hm-task-todo'>"
                f"{task_text}"
                f"<div style='font-size:0.68rem;"
                f"color:#3f3f46;margin-top:4px;"
                f"letter-spacing:0.04em;'>"
                f"→ {assigned}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with tc2:
            if st.button(
                "→",
                key=f"todo_mv_{task_id}",
                help="Move to In Progress"
            ):
                update_task_status(
                    task_id, "in_progress"
                )
                st.rerun()
        with tc3:
            if st.button(
                "✕",
                key=f"todo_del_{task_id}",
                help="Delete task"
            ):
                delete_team_task(task_id)
                st.rerun()

    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    # ── IN PROGRESS ───────────────────────────────────
    st.markdown(
        "<div style='font-size:0.68rem;font-weight:500;"
        "letter-spacing:0.1em;text-transform:uppercase;"
        "color:#a1a1aa;margin-bottom:0.6rem;'>"
        "In Progress</div>",
        unsafe_allow_html=True
    )

    if not progress_tasks:
        st.markdown(
            "<div style='font-size:0.8rem;color:#27272a;"
            "font-style:italic;padding:0.8rem 0;'>"
            "Nothing in progress yet.</div>",
            unsafe_allow_html=True
        )

    for task in progress_tasks:
        task_id = task["id"]
        task_text = task["task_text"]
        assigned = task["assigned_to"]

        tc1, tc2, tc3 = st.columns([5, 1, 1])
        with tc1:
            st.markdown(
                f"<div class='hm-task hm-task-progress'>"
                f"{task_text}"
                f"<div style='font-size:0.68rem;"
                f"color:#52525b;margin-top:4px;"
                f"letter-spacing:0.04em;'>"
                f"→ {assigned}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with tc2:
            if st.button(
                "✓",
                key=f"prog_mv_{task_id}",
                help="Mark as Done"
            ):
                update_task_status(task_id, "done")
                st.rerun()
        with tc3:
            if st.button(
                "✕",
                key=f"prog_del_{task_id}",
                help="Delete task"
            ):
                delete_team_task(task_id)
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

    if not done_tasks:
        st.markdown(
            "<div style='font-size:0.8rem;color:#27272a;"
            "font-style:italic;padding:0.8rem 0;'>"
            "No completed tasks yet.</div>",
            unsafe_allow_html=True
        )

    for task in done_tasks:
        task_text = task["task_text"]
        assigned = task["assigned_to"]
        st.markdown(
            f"<div class='hm-task hm-task-done'>"
            f"{task_text}"
            f"<div style='font-size:0.68rem;"
            f"margin-top:4px;'>"
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

    # Load messages from Supabase
    db_messages = get_team_messages(user.id) \
        if user else []

    if not db_messages:
        st.markdown(
            "<div style='background:#111113;"
            "border:1px solid #1c1c1f;"
            "border-radius:12px;padding:2rem;"
            "text-align:center;margin-bottom:1rem;'>"
            "<div style='font-size:0.85rem;"
            "color:#3f3f46;font-style:italic;"
            "font-weight:300;'>"
            "No messages yet. Say hello to your team."
            "</div></div>",
            unsafe_allow_html=True
        )

    for msg in db_messages:
        is_me = str(msg["sender_id"]) == str(user.id)
        sender = msg["sender_name"]

        try:
            raw_time = msg["created_at"]
            if "T" in raw_time:
                dt = datetime.fromisoformat(
                    raw_time.replace("Z", "+00:00")
                )
                time_str = dt.strftime("%I:%M %p")
            else:
                time_str = raw_time[-8:-3]
        except Exception:
            time_str = ""

        if is_me:
            st.markdown(
                f"<div class='hm-chat-me'>"
                f"<div class='hm-chat-sender'>"
                f"You · {time_str}</div>"
                f"{msg['message']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='hm-chat-other'>"
                f"<div class='hm-chat-sender'>"
                f"{sender} · {time_str}</div>"
                f"{msg['message']}</div>",
                unsafe_allow_html=True
            )

    st.markdown(
        "<div style='height:1rem'></div>",
        unsafe_allow_html=True
    )

    msg_input = st.text_input(
        "Message",
        placeholder="Say something to your team...",
        key="chat_input",
        label_visibility="collapsed"
    )

    sc1, sc2 = st.columns([4, 1])
    with sc2:
        send = st.button(
            "Send",
            use_container_width=True
        )

    if send and msg_input.strip():
        success = send_team_message(
            sender_id=user.id,
            sender_name=name,
            team_member_ids=team_ids,
            message=msg_input.strip()
        )
        if success:
            st.rerun()
        else:
            st.error("Could not send message.")

    st.markdown(
        "<div style='height:0.5rem'></div>",
        unsafe_allow_html=True
    )

    if st.button(
        "Refresh messages",
        use_container_width=True,
        key="refresh_chat"
    ):
        st.rerun()

    st.markdown(
        "<div style='font-size:0.7rem;color:#3f3f46;"
        "text-align:center;margin-top:0.3rem;'>"
        "Click refresh to see new messages</div>",
        unsafe_allow_html=True
    )

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

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(
            f"<div class='hm-stat-card'>"
            f"<div class='hm-stat-card-number'>"
            f"{done_count}</div>"
            f"<div class='hm-stat-card-label'>"
            f"Done</div></div>",
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            f"<div class='hm-stat-card'>"
            f"<div class='hm-stat-card-number'>"
            f"{in_prog}</div>"
            f"<div class='hm-stat-card-label'>"
            f"Active</div></div>",
            unsafe_allow_html=True
        )
    with s3:
        st.markdown(
            f"<div class='hm-stat-card'>"
            f"<div class='hm-stat-card-number'>"
            f"{len(member_names)}</div>"
            f"<div class='hm-stat-card-label'>"
            f"Members</div></div>",
            unsafe_allow_html=True
        )