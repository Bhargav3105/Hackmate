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

[**View HackMate Live →**](https://hackmate-v2.streamlit.app/)

<br>

</div>

---

## What is HackMate?

HackMate is a full-stack AI-powered web application that solves one of the biggest problems at every hackathon — finding the right teammates.

Instead of randomly teaming up or posting in Discord servers hoping someone responds, HackMate uses AI to intelligently match you with compatible developers based on your skills, experience level, goals and daily availability. It then helps your team generate winning project ideas, assign roles, track tasks and collaborate — all in one place.

**The problem it solves:**
Most hackathon participants waste hours finding teammates, end up with mismatched skill sets, and build projects without a clear plan. HackMate fixes all three problems with AI.

---

## Live Demo

[**View HackMate Live →**](https://hackmate-v2.streamlit.app/)

> Replace the URL above with your actual Streamlit Cloud URL after deployment.

---

## Features

### Core MVP Features

| Feature | Description |
|---|---|
| Smart User Profiles | Skills, tech stack, experience, availability, goals and GitHub |
| AI Team Matching | Compatibility scoring powered by Groq Llama 3.3 70B |
| Compatibility Score | Percentage match with strengths, roles and challenges |
| AI Project Idea Generator | 3 detailed ideas with features, stack and 3-day MVP plan |
| Team Invite System | Send invites, invitee accepts/declines, team votes to approve |
| Connection Requests | Send and accept direct team requests with custom messages |
| Team Workspace | Shared task board, team chat and progress tracking |
| Shared Tasks | All tasks visible to every team member in real time |
| Shared Chat | Messages stored in database — visible to all team members |
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
| Profile Completion | Track how complete your profile is |
| Shareable Profile | Share your HackMate profile link |

### AI Features in Detail

**Team Matching Engine**
- Analyzes two developer profiles across 5 dimensions
- Returns compatibility score from 0 to 100
- Explains exactly why the match works
- Suggests specific roles for each person
- Flags potential collaboration challenges

**Project Idea Generator**
- Takes team skills, experience level and goals as input
- Generates 3 unique buildathon ideas focused on Sarvam AI track
- Each idea includes problem statement, solution, 4 key features, tech stack, 3-day MVP timeline and judge wow factor
- Difficulty rating for each idea

**AI Role Assignment**
- Analyzes every team member's skills
- Assigns the most suitable role for each person
- Lists 3 key responsibilities per role
- Explains why this role suits each person
- Gives a one-line team strength summary

**Profile Recommendations**
- Analyzes your profile and recommends skills to look for in teammates
- Suggests your ideal team size and role
- Gives 3 personalized hackathon success tips

---

## Tech Stack
Frontend          Streamlit (Python)
Database          Supabase (PostgreSQL)
Authentication    Supabase Auth (Email + Password)
AI Engine         Groq API — Llama 3.3 70B Versatile
Deployment        Streamlit Cloud
Version Control   Git + GitHub
Language          Python 3.11

### Why this stack?

- **Streamlit** — Build a full UI in pure Python. Perfect for AI apps and rapid prototyping without React overhead.
- **Supabase** — Postgres database with built-in auth, row level security and a generous free tier.
- **Groq** — Fastest LLM inference available. Free tier. Llama 3.3 70B gives GPT-4 quality responses.
- **Streamlit Cloud** — One-click deployment directly from GitHub. Free hosting for public repos.

---

## How It Works

```
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
            |
            v
  03  FIND TEAMMATES
      Browse real developer profiles
      Check AI compatibility score
      Send invite to team
            |
            v
  04  INVITE FLOW
      Three-step approval process
      → Invitee accepts or declines
      → Existing teammates vote to approve
      → All approve = person joins all teams
            |
            v
  05  TEAM WORKSPACE
      Collaborate and ship together
      → Add tasks · Assign to members
      → Move tasks: To Do → In Progress → Done
      → Team chat visible to all members
      → AI role assignment for each member
            |
            v
  06  GENERATE IDEAS
      AI creates your buildathon strategy
      → 3 unique project ideas for your stack
      → Features · Tech stack · Timeline
      → 3-day MVP roadmap · Judge wow factor

─────────────────────────────────────────────────
```

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
    recipient_ids text[], -- all team member IDs
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
```

---

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

Create a file called `.env` in the root folder:
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=

### Step 5 — Set up Supabase database

Run the complete SQL from the Database Schema section above in your Supabase SQL Editor.

### Step 6 — Run the app

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Deployment

HackMate is deployed on Streamlit Cloud:

1. Push code to GitHub (public repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file as `app.py`
5. Add secrets in Advanced Settings:

```toml
SUPABASE_URL = "https://yourproject.supabase.co"
SUPABASE_KEY = "your_anon_key"
SUPABASE_SERVICE_KEY = "your_service_role_key"
GROQ_API_KEY = "your_groq_key"
OPENAI_API_KEY = ""
```

6. Click Deploy

---

## Security

- All API keys stored in `.env` — never committed to Git
- `.env` is listed in `.gitignore`
- Supabase Row Level Security enabled on all tables
- Service role key only used server-side
- All user data protected by RLS policies

---

## Key Design Decisions

**Why session-based auth?**
Streamlit reruns the entire script on every interaction. Storing the access token in `session_state` and restoring the profile from Supabase on each page load is the most reliable pattern for multi-page Streamlit apps.

**Why service role key for writes?**
Row Level Security in Supabase requires the user's JWT token. Since Streamlit's Python backend doesn't maintain a persistent connection, using the service role key for server-side writes is safer and more reliable for this architecture.

**Why Groq instead of OpenAI?**
Groq is free, extremely fast and Llama 3.3 70B produces output quality comparable to GPT-4. Zero cost and no latency issues — perfect for a buildathon.

**Why JSON responses from AI?**
Structured JSON output makes it easy to display AI responses in a clean UI. The `clean_json()` helper strips markdown formatting that LLMs sometimes add, making parsing robust even with imperfect model output.

**Three-step team invite flow:**
Real teams need consensus. The invite → accept → vote system ensures no one gets added to a team without everyone's agreement — just like real startup teams work.

---

## Roadmap

- [x] Email authentication with Supabase
- [x] Smart user profile setup and editing
- [x] AI teammate matching with Groq
- [x] Compatibility scoring with explanations
- [x] Real user profiles from database
- [x] Three-step team invite and voting system
- [x] Team workspace with shared task board
- [x] Real-time team chat stored in database
- [x] AI project idea generator
- [x] AI role assignment for team members
- [x] Hackathon countdown timer
- [x] Profile persistence across sessions
- [x] Notifications badge for pending requests
- [x] Search and filter teammates
- [ ] Google OAuth login
- [ ] Mobile responsive design
- [ ] Email notifications for requests
- [ ] Team health score
- [ ] Mentor recommendations
- [ ] Export project plan as PDF

---

## Development Journey

This project was built during the Sarvam AI Buildathon 2025. The development progressed through these phases:

| Phase | What was built |
|---|---|
| Week 1 | Environment setup, GitHub, Supabase, landing page, auth |
| Week 2 | Profile setup, dashboard, AI matching, compatibility scoring |
| Week 3 | Project idea generator, team workspace, connection requests |
| Week 4 | Team invite voting system, shared tasks, shared chat |
| Week 5 | AI role assignment, countdown timer, UI polish, deployment |

---

## Team

This project was designed, architected and built by a team of four developers.

<br>

### Bhargav Bathla — Project Lead & Full Stack Developer

> Responsible for overall product vision, architecture decisions, full stack development and project delivery.

**Role:** Product Lead · Full Stack Engineer · AI Integration

**Skills used in this project:**
- Product architecture and feature prioritization
- Streamlit frontend development and UI design system
- Python backend logic and page routing
- Supabase database schema design and RLS policies
- Groq AI API integration and prompt engineering
- Session management and authentication flow
- Git workflow and deployment on Streamlit Cloud

---

### Aishwary Raghuwansi — AI & Backend Engineer

> Responsible for AI model integration, prompt design and backend data pipeline.

**Role:** AI Engineer · Backend Developer

**Skills used in this project:**
- Groq API and LLM integration
- Prompt engineering for structured JSON output
- AI compatibility scoring algorithm design
- Python backend utility functions
- JSON parsing and error handling for AI responses
- AI role assignment feature development
- Testing and validating AI output quality

---

### Rajat Kumar Singh — Database & Auth Engineer

> Responsible for database architecture, authentication system and data security.

**Role:** Database Engineer · Security & Auth Specialist

**Skills used in this project:**
- Supabase PostgreSQL schema design
- Row Level Security policy configuration
- User authentication flow with Supabase Auth
- Team connection, voting and invitation table design
- Data persistence and session management
- Service role key management and secure writes
- Security incident response and key rotation

---

### Tejas Baghel — UI/UX Designer & Frontend Developer

> Responsible for visual design, user experience and frontend implementation.

**Role:** UI/UX Designer · Frontend Developer

**Skills used in this project:**
- Premium dark UI design system
- CSS animations and smooth scroll reveal effects
- Component design — cards, badges, match cards, task board
- Typography hierarchy with Playfair Display and Inter fonts
- Sidebar suppression and navigation design
- User flow design across all eight pages
- Design consistency and visual polish inspired by premium startups

---

## License

MIT License — free to use, modify and distribute.

---

<div align="center">

<br>

**HackMate** · Built for Sarvam AI Buildathon · 2025

*"The best hackathon teams don't happen by accident."*

<br>

</div>