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

<br>

> Built for the **Sarvam AI Buildathon 2025**
> Track: **Developer Tools & Software Infrastructure**

<br>

</div>

---

## What is HackMate?

HackMate is a full-stack AI-powered web application that solves one of the biggest problems at every hackathon — finding the right teammates.

Instead of randomly teaming up or posting in Discord servers hoping someone responds, HackMate uses AI to intelligently match you with compatible developers based on your skills, experience level, goals and daily availability. It then helps your team generate winning project ideas, assign tasks and collaborate — all in one place.

**The problem it solves:**
Most hackathon participants waste hours finding teammates, end up with mismatched skill sets, and build projects without a clear plan. HackMate fixes all three problems with AI.

---

## Live Demo
Coming soon — deployment in progress

---

## Screenshots

### Landing Page
A clean, premium dark interface that immediately communicates the product value.

### Dashboard
Personalized AI match recommendations with compatibility scores and quick actions.

### AI Teammate Matching
Real-time compatibility scoring with strengths, role suggestions and match reasoning.

### Project Idea Generator
Three detailed AI-generated buildathon ideas with full feature lists and 3-day timelines.

### Team Workspace
Collaborative task board with assignees, team chat and real-time progress tracking.

---

## Features

### Core MVP Features

| Feature | Description |
|---|---|
| Smart User Profiles | Skills, tech stack, experience, availability, goals and GitHub |
| AI Team Matching | Compatibility scoring powered by Groq Llama 3.3 70B |
| Compatibility Score | Percentage match with strengths, roles and challenges |
| AI Project Idea Generator | 3 detailed ideas with features, stack and 3-day MVP plan |
| Connection Requests | Send and accept team requests with custom messages |
| Team Workspace | Task board with assignees, team chat and progress bar |
| Dashboard | AI recommendations, team members and quick actions |
| Real User Database | Live profiles from Supabase shown alongside sample matches |

### AI Features in Detail

**Team Matching Engine**
- Analyzes two developer profiles across 5 dimensions
- Returns compatibility score from 0 to 100
- Explains exactly why the match works
- Suggests specific roles for each person
- Flags potential collaboration challenges

**Project Idea Generator**
- Takes team skills, experience level and goals as input
- Generates 3 unique buildathon ideas focused on the Sarvam AI track
- Each idea includes: problem statement, solution, 4 key features, recommended tech stack, 3-day MVP timeline and a judge wow factor
- Difficulty rating for each idea

**Profile Recommendations**
- Analyzes your profile and recommends what skills to look for in teammates
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

## Project Structure
hackmate/
│
├── app.py                        # Landing page — hero, features, CTA
│
├── pages/
│   ├── 2_login.py                # Email authentication — sign in and sign up
│   ├── 3_profile_setup.py        # User profile creation and editing
│   ├── 4_find_teammates.py       # Browse real users, check AI compatibility
│   ├── 5_match_results.py        # AI project idea generator
│   ├── 6_dashboard.py            # Main dashboard — matches, team, actions
│   └── 7_team_workspace.py       # Team tasks, chat and progress tracking
│
├── utils/
│   ├── ai_helper.py              # All Groq AI calls — matching, ideas, tips
│   ├── auth.py                   # Session management and profile loading
│   ├── styles.py                 # Global CSS design system
│   └── supabase_client.py        # All database operations — CRUD, requests
│
├── .streamlit/
│   └── config.toml               # Streamlit theme and server config
│
├── .env                          # Secret keys — never committed to GitHub
├── .gitignore                    # Protects secrets and venv
├── requirements.txt              # All Python dependencies
└── README.md                     # This file

---

## Database Schema

```sql
-- User profiles
profiles (
    id uuid PRIMARY KEY,          -- Links to Supabase auth user
    full_name text,
    bio text,
    skills text[],                -- Array of skill strings
    experience_level text,
    availability text,
    goals text[],                 -- Array of goal strings
    github_url text,
    created_at timestamp
)

-- Connection requests between users
requests (
    id uuid PRIMARY KEY,
    from_user_id uuid,            -- Who sent the request
    to_user_id uuid,              -- Who received it
    from_name text,
    message text,
    status text,                  -- pending / accepted / declined
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
```

---

## How It Works

Sign up → Create your developer profile
(skills, experience, goals, availability)
Dashboard → AI immediately shows your top matches
with compatibility scores and reasons
Find Teammates → Browse real developer profiles
→ Click "Check Compatibility" for AI analysis
→ Click "Connect" to send a request
Accept Request → Connected user appears in your team
→ Team Workspace unlocked for both users
Team Workspace → Add tasks and assign to team members
→ Move tasks: To Do → In Progress → Done
→ Chat with your team
→ Track overall project progress
Generate Ideas → Enter your team's combined skills
→ Get 3 AI-generated buildathon ideas
→ Each with full features, stack and timeline


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

### Step 5 — Set up Supabase

Run this SQL in your Supabase SQL Editor:

```sql
-- Profiles
create table profiles (
    id uuid references auth.users on delete cascade primary key,
    full_name text, bio text, skills text[],
    experience_level text, availability text,
    goals text[], github_url text,
    created_at timestamp default now()
);

-- Enable RLS
alter table profiles enable row level security;
create policy "Authenticated users can read profiles"
    on profiles for select to authenticated using (true);
create policy "Users can insert own profile"
    on profiles for insert to authenticated with check (true);
create policy "Users can update own profile"
    on profiles for update to authenticated
    using (auth.uid() = id);

-- Requests
create table requests (
    id uuid default gen_random_uuid() primary key,
    from_user_id uuid references profiles(id) on delete cascade,
    to_user_id uuid references profiles(id) on delete cascade,
    from_name text, message text,
    status text default 'pending',
    created_at timestamp default now()
);

alter table requests enable row level security;
create policy "Users can manage requests"
    on requests for all to authenticated using (true);

-- Team connections
create table team_connections (
    id uuid default gen_random_uuid() primary key,
    user1_id uuid references profiles(id) on delete cascade,
    user2_id uuid references profiles(id) on delete cascade,
    user1_name text, user2_name text,
    connected_at timestamp default now()
);

alter table team_connections enable row level security;
create policy "Users can manage connections"
    on team_connections for all to authenticated using (true);
```

### Step 6 — Run the app

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Deployment

HackMate is deployed on Streamlit Cloud:

1. Push your code to GitHub (public repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set your environment variables in the Streamlit Cloud secrets panel
5. Click Deploy

---

## Key Design Decisions

**Why session-based auth instead of token refresh?**
Streamlit reruns the entire script on every interaction. Storing the access token in `session_state` and restoring the profile from Supabase on each page load is the most reliable pattern for multi-page Streamlit apps.

**Why service role key for database writes?**
Row Level Security in Supabase requires the user's JWT token to be passed with every request. Since Streamlit's Python backend doesn't maintain a persistent connection, using the service role key for server-side writes is safer and more reliable for this architecture.

**Why Groq instead of OpenAI?**
Groq is free, extremely fast (10x faster than OpenAI), and Llama 3.3 70B produces output quality comparable to GPT-4. For a buildathon MVP this is the right choice — zero cost and no latency issues.

**Why JSON responses from AI?**
Structured JSON output makes it easy to display AI responses in a clean UI. The `clean_json()` helper strips markdown formatting that LLMs sometimes add, making parsing robust even with imperfect model output.

---

## Roadmap

- [x] Email authentication with Supabase
- [x] Smart user profile setup
- [x] AI teammate matching with Groq
- [x] Compatibility scoring with explanations
- [x] Real user profiles from database
- [x] Connection request system
- [x] Team workspace with task board
- [x] Team chat
- [x] AI project idea generator
- [x] Profile persistence across sessions
- [ ] Google OAuth login
- [ ] AI sprint planner
- [ ] Role assignment AI
- [ ] Team health score
- [ ] Inactive member detection
- [ ] Mentor recommendations
- [ ] Mobile responsive design
- [ ] Email notifications for requests

---

## Development Journey

This project was built during the Sarvam AI Buildathon 2025 over approximately 2 weeks as a solo developer project. The development progressed through these phases:

| Phase | What was built |
|---|---|
| Week 1 | Environment setup, GitHub, Supabase, landing page, auth |
| Week 2 | Profile setup, dashboard, AI matching, compatibility |
| Week 3 | Project idea generator, team workspace, connection requests |
| Week 4 | UI polish, session persistence, bug fixes, deployment |

---

## Author

**Bhargav Bathla**

Built from scratch during the Sarvam AI Buildathon 2025.

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