<div align="center">

<br>

# HackMate

### AI-powered collaboration platform for hackathons and buildathons

<br>

Find compatible teammates · Generate winning project ideas · Build together

<br>

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq%20AI-orange?style=flat-square)](https://groq.com)
[![Database](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

<br>

> Built for the **Sarvam AI Buildathon 2025**
> Track: **Developer Tools & Software Infrastructure**

<br>

[**View HackMate Live →**](https://hackmate-v2.streamlit.app)

<br>

</div>

---

## What is HackMate?

HackMate is a full-stack AI-powered web application that solves one of the biggest problems at every hackathon — finding the right teammates.

Instead of randomly teaming up or posting in Discord servers hoping someone responds, HackMate uses AI to intelligently match developers based on skills, experience level, goals and daily availability. It then helps the team generate winning project ideas, assign roles, track tasks and collaborate — all in one place.

**The problem it solves:**
Most hackathon participants waste hours finding teammates, end up with mismatched skill sets, and build projects without a clear plan. HackMate fixes all three with AI at the core of the product, not bolted on as an afterthought.

---

## Live Demo

[**View HackMate Live →**](https://hackmate-v2.streamlit.app)

---

## Features

### Core Features

| Feature | Description |
|---|---|
| Smart User Profiles | Skills, tech stack, experience, availability, goals and GitHub |
| AI Team Matching | Compatibility scoring powered by Groq Llama 3.3 70B |
| Compatibility Score | Percentage match with strengths, roles and challenges |
| AI Project Idea Generator | 3 detailed ideas with features, stack and 3-day MVP plan |
| PDF Export | Download any generated project plan as a polished PDF |
| Team Invite System | Invite sent → invitee accepts/declines → existing team votes |
| Connection Requests | Send and accept direct team requests with custom messages |
| Team Workspace | Shared task board, team chat, activity feed and progress tracking |
| Shared Tasks | All tasks visible to every team member in real time |
| Shared Chat | Messages stored in database — visible to all team members |
| Team Activity Feed | Live log of tasks added, completed and messages sent |
| Dashboard | AI recommendations, countdown timer, team members, quick actions |
| Notifications | Badge shows pending requests and votes |
| Profile Edit | Update skills, goals and availability after setup |
| Search and Filter | Find teammates by name, experience and availability |

### Advanced Features

| Feature | Description |
|---|---|
| AI Role Assignment | AI analyses team skills and assigns the best role for each member |
| Hackathon Countdown | Set your deadline — live countdown on dashboard |
| Team Voting System | Existing members vote to approve new team additions |
| Session Persistence | Stays logged in across page refreshes |

### AI Features in Detail

**Team Matching Engine**
Analyzes two developer profiles across five dimensions and returns a compatibility score from 0 to 100, an explanation of why the match works, specific role suggestions for each person, and potential collaboration challenges to watch for.

**Project Idea Generator**
Takes team skills, experience level and goals as input and generates three unique buildathon ideas, each with a problem statement, solution, four key features, recommended tech stack, a three-day MVP timeline and a judge wow factor. Every idea can be exported as a clean PDF document.

**AI Role Assignment**
Analyzes every team member's skills and assigns the most suitable role for each person, with three key responsibilities and an explanation of why that role fits, plus a one-line summary of the team's overall strength.

**Profile Recommendations**
Analyzes a user's profile and suggests what skills to look for in teammates, an ideal team size, a recommended role, and personalized hackathon success tips.

---

## Tech Stack
Frontend          Streamlit (Python)

Database          Supabase (PostgreSQL)

Authentication    Supabase Auth (Email + Password, session persistence)

AI Engine         Groq API — Llama 3.3 70B Versatile

PDF Generation     ReportLab

Deployment        Streamlit Cloud

Version Control   Git + GitHub

Language          Python 3.11

### Why this stack?

Streamlit lets the whole UI be built in pure Python, which keeps the entire stack in one language and made rapid iteration possible without a separate frontend build step. Supabase provides a Postgres database with built-in auth and row level security on a generous free tier. Groq was chosen over OpenAI because it is free, extremely fast, and Llama 3.3 70B produces output quality comparable to GPT-4 with no latency issues — ideal for a buildathon timeline. Streamlit Cloud gives one-click deployment directly from GitHub with free hosting for public repositories.

---

## How It Works
HACKMATE FLOW

─────────────────────────────────────────────────

01  SIGN UP

Create your developer profile

Skills · Experience · Goals · Availability

|
v

02  DASHBOARD

AI shows your top matches instantly

Compatibility scores · Match reasoning

Hackathon countdown timer

|
v

03  FIND TEAMMATES

Browse real developer profiles

Search and filter by experience and availability

Check AI compatibility score

Send invite to team

|
v

04  INVITE FLOW

Three-step approval process

→ Invitee accepts or declines

→ Existing teammates vote to approve

→ All approve = person joins every member's team

|
v

05  TEAM WORKSPACE

Collaborate and ship together

→ Add tasks · Assign to members · Delete if needed

→ Move tasks: To Do → In Progress → Done

→ Team chat visible to all members

→ Activity feed tracks every team action

→ AI role assignment for each member

|
v

06  GENERATE IDEAS

AI creates your buildathon strategy

→ 3 unique project ideas for your stack

→ Features · Tech stack · Timeline

→ 3-day MVP roadmap · Judge wow factor

→ Export any idea as a PDF
─────────────────────────────────────────────────

---

## Database Schema

```sql
-- User profiles
profiles (
    id uuid PRIMARY KEY,
    full_name text,
    bio text,
    skills text[],
    experience_level text,
    availability text,
    goals text[],
    github_url text,
    hackathon_deadline timestamp,
    created_at timestamp
)

-- Direct connection requests
requests (
    id uuid PRIMARY KEY,
    from_user_id uuid,
    to_user_id uuid,
    from_name text,
    message text,
    status text,          -- pending / accepted / declined
    created_at timestamp
)

-- Accepted team connections
team_connections (
    id uuid PRIMARY KEY,
    user1_id uuid,
    user2_id uuid,
    user1_name text,
    user2_name text,
    connected_at timestamp
)

-- Team invitations (new member invite flow)
team_invitations (
    id uuid PRIMARY KEY,
    invitee_id text,
    invitee_name text,
    proposer_id uuid,
    proposer_name text,
    status text,          -- pending_acceptance / voting / approved / declined
    created_at timestamp
)

-- Votes for new member approval
team_votes (
    id uuid PRIMARY KEY,
    invitation_id uuid,
    voter_id uuid,
    voter_name text,
    vote text,            -- pending / accepted / rejected
    voted_at timestamp
)

-- Team chat messages
team_messages (
    id uuid PRIMARY KEY,
    sender_id uuid,
    sender_name text,
    recipient_ids text[],
    message text,
    created_at timestamp
)

-- Shared team tasks
team_tasks (
    id uuid PRIMARY KEY,
    created_by_id uuid,
    created_by_name text,
    team_member_ids text[],
    task_text text,
    assigned_to text,
    status text,          -- todo / in_progress / done
    created_at timestamp
)

-- Team activity feed
team_activity (
    id uuid PRIMARY KEY,
    actor_id uuid,
    actor_name text,
    action_type text,     -- task_added / task_done / message
    action_text text,
    team_member_ids text[],
    created_at timestamp
)
```


## Getting Started Locally

### Prerequisites
- Python 3.10 or higher
- A [Supabase](https://supabase.com) account (free)
- A [Groq](https://console.groq.com) API key (free)

### Step 1 — Clone the repo

```bash
git clone https://github.com/YOURUSERNAME/hackmate.git
cd hackmate
```

### Step 2 — Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create your .env file
SUPABASE_URL=https://yourproject.supabase.co

SUPABASE_KEY=your_supabase_anon_key

SUPABASE_SERVICE_KEY=your_supabase_service_role_key

GROQ_API_KEY=your_groq_api_key

OPENAI_API_KEY=

### Step 5 — Set up the database

Run the full SQL from the Database Schema section above in your Supabase SQL Editor, with row level security enabled and an open policy on each table for authenticated users.

### Step 6 — Run the app

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Deployment

HackMate runs on Streamlit Cloud:

1. Push code to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo
3. Set the main file to `app.py`
4. Add the four secrets shown in Step 4 above under Advanced Settings
5. Deploy

---

## Security

All API keys are stored in `.env`, which is listed in `.gitignore` and never committed. Supabase Row Level Security is enabled on every table, and the service role key is only ever used server-side. During development a key was briefly exposed in an earlier commit; it was detected via GitGuardian, the affected keys were rotated immediately, a fresh Supabase project was created, and Git history was scrubbed — a real incident that shaped how secrets are handled in this project going forward.

---

## Key Design Decisions

**Session-based authentication.** Streamlit reruns the entire script on every interaction, so the access token is stored in both `session_state` and the URL query params, and the profile is restored from Supabase on every page load. This is the most reliable pattern for keeping users logged in across a multi-page Streamlit app and page refreshes.

**Service role key for writes.** Row Level Security normally needs the user's JWT on every request, but Streamlit's backend doesn't keep a persistent authenticated connection. Using the service role key for server-side writes, combined with strict RLS policies, was the more reliable choice for this architecture.

**Groq over OpenAI.** Groq is free, very fast, and Llama 3.3 70B gives output quality close to GPT-4 — ideal for a project on a tight timeline with zero budget for API costs.

**Three-step team invite flow.** Real teams need consensus, not unilateral additions. The invite → accept → vote system means no one joins a team without the invitee's agreement and the existing team's approval — closer to how real teams actually decide to add someone.

**JSON-only AI responses.** Structured JSON output makes it possible to render AI responses as clean UI components rather than walls of text. A `clean_json()` helper strips markdown fences that LLMs sometimes add, so parsing stays robust even with imperfect model output.

---

## Roadmap

- [x] Email authentication with session persistence
- [x] Smart user profile setup and editing
- [x] AI teammate matching with Groq
- [x] Compatibility scoring with explanations
- [x] Real user profiles from database
- [x] Three-step team invite and voting system
- [x] Team workspace with shared task board
- [x] Real-time team chat stored in database
- [x] Team activity feed
- [x] AI project idea generator
- [x] PDF export of project plans
- [x] AI role assignment for team members
- [x] Hackathon countdown timer
- [x] Notifications badge for pending requests
- [x] Search and filter teammates
- [x] Deployed live on Streamlit Cloud
- [ ] Demo video walkthrough
- [ ] Mobile-responsive layout pass
- [ ] Google OAuth login
- [ ] Email notifications for requests
- [ ] Team health score

---

## Development Journey
Week 1   Environment setup, GitHub, Supabase, landing page, auth

Week 2   Profile setup, dashboard, AI matching, compatibility scoring

Week 3   Project idea generator, team workspace, connection requests

Week 4   Team invite voting system, shared tasks, shared chat

Week 5   AI role assignment, countdown timer, activity feed, PDF export

Week 6   Security incident response, key rotation, deployment, polish

---

## Team

This project was designed, architected and built by a team of four developers.

<br>

### Bhargav Bathla — Project Lead & Full Stack Developer

> Responsible for overall product vision, architecture decisions, full stack development and project delivery.

**Role:** Product Lead · Full Stack Engineer · AI Integration

**Skills used in this project:** product architecture and feature prioritization, Streamlit frontend development and the UI design system, Python backend logic and page routing, Supabase schema design and RLS policies, Groq AI integration and prompt engineering, session management and authentication flow, Git workflow, security incident response, and deployment on Streamlit Cloud.

---

### Aishwary Raghuwansi — AI & Backend Engineer

> Responsible for AI model integration, prompt design and the backend data pipeline.

**Role:** AI Engineer · Backend Developer

**Skills used in this project:** Groq API and LLM integration, prompt engineering for structured JSON output, the AI compatibility scoring algorithm, AI role assignment logic, Python backend utility functions, JSON parsing and error handling for AI responses, and testing AI output quality and consistency.

---

### Rajat Kumar Singh — Database & Auth Engineer

> Responsible for database architecture, authentication and data security.

**Role:** Database Engineer · Security & Auth Specialist

**Skills used in this project:** Supabase PostgreSQL schema design, Row Level Security policy configuration, the authentication flow with Supabase Auth, design of the team connection, voting and invitation tables, data persistence and session management, service role key handling, and the security incident response that led to rotating keys and migrating to a fresh Supabase project.

---

### Tejas Baghel — UI/UX Designer & Frontend Developer

> Responsible for visual design, user experience and frontend implementation.

**Role:** UI/UX Designer · Frontend Developer

**Skills used in this project:** the premium dark UI design system, CSS scroll-reveal animations and hover micro-interactions, component design for cards, badges and the task board, typography with Playfair Display and Inter, sidebar suppression and navigation design, user flow design across all eight pages, and overall design consistency.

---

## License

MIT License — free to use, modify and distribute.

---

<div align="center">

<br>

**HackMate** · Built for Sarvam AI Buildathon · 2025

*"The best hackathon teams don't happen by accident."*

[**View HackMate Live →**](https://hackmate-v2.streamlit.app)

<br>

</div>