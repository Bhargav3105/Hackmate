def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500;600&display=swap');

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }

    .stApp {
        background-color: #0c0c0e;
        color: #d4d4d8;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 5rem !important;
        max-width: 1080px !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #f4f4f5;
        font-weight: 500;
    }

    /* ── ANIMATIONS ─────────────────────────── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.97); }
        to   { opacity: 1; transform: scale(1); }
    }

    .anim-1 { animation: fadeUp 0.7s ease both; }
    .anim-2 { animation: fadeUp 0.7s ease 0.15s both; }
    .anim-3 { animation: fadeUp 0.7s ease 0.3s both; }
    .anim-4 { animation: fadeUp 0.7s ease 0.45s both; }
    .anim-fade { animation: fadeIn 1s ease both; }
    .anim-scale { animation: scaleIn 0.6s ease both; }

    /* ── LOGO ───────────────────────────────── */
    .hm-logo {
        font-family: 'Playfair Display', serif;
        font-size: 1.35rem;
        font-weight: 500;
        color: #f4f4f5;
        letter-spacing: 0.02em;
    }

    /* ── HERO ───────────────────────────────── */
    .hm-headline {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2.8rem, 6vw, 4.8rem);
        font-weight: 500;
        line-height: 1.1;
        color: #f4f4f5;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
    }

    .hm-subheadline {
        font-size: 1rem;
        font-weight: 300;
        color: #71717a;
        line-height: 1.85;
        max-width: 460px;
        margin-bottom: 2.5rem;
    }

    /* ── BADGE ──────────────────────────────── */
    .hm-badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #71717a;
        border: 1px solid #27272a;
        border-radius: 999px;
        padding: 5px 14px;
        margin-bottom: 2rem;
    }

    /* ── LABELS ─────────────────────────────── */
    .hm-label {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #52525b;
        margin-bottom: 0.6rem;
    }

    .hm-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 500;
        color: #f4f4f5;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }

    /* ── FEATURE ROWS ───────────────────────── */
    .hm-feature {
        padding: 1.8rem 0;
        border-top: 1px solid #1c1c1f;
        transition: border-color 0.3s;
    }

    .hm-feature:hover { border-top-color: #3f3f46; }

    .hm-feature-number {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        color: #3f3f46;
        margin-bottom: 0.8rem;
    }

    .hm-feature-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 500;
        color: #f4f4f5;
        margin-bottom: 0.5rem;
    }

    .hm-feature-desc {
        font-size: 0.85rem;
        color: #52525b;
        line-height: 1.8;
        font-weight: 300;
    }

    /* ── STAT ───────────────────────────────── */
    .hm-stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 500;
        color: #f4f4f5;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .hm-stat-label {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #3f3f46;
    }

    /* ── CARDS ──────────────────────────────── */
    .hm-card {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 16px;
        padding: 1.8rem;
        transition: border-color 0.3s ease, transform 0.3s ease;
    }

    .hm-card:hover {
        border-color: #3f3f46;
        transform: translateY(-2px);
    }

    /* ── STAT CARDS ─────────────────────────── */
    .hm-stat-card {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        transition: border-color 0.3s;
    }

    .hm-stat-card:hover { border-color: #3f3f46; }

    .hm-stat-card-number {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 500;
        color: #f4f4f5;
        line-height: 1;
        margin-bottom: 0.3rem;
    }

    .hm-stat-card-label {
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #3f3f46;
    }

    /* ── MATCH CARDS ────────────────────────── */
    .hm-match {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 0.7rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: border-color 0.25s, background 0.25s,
                    transform 0.25s;
        animation: scaleIn 0.5s ease both;
    }

    .hm-match:hover {
        border-color: #3f3f46;
        background: #141416;
        transform: translateX(4px);
    }

    .hm-match-name {
        font-family: 'Playfair Display', serif;
        font-size: 0.98rem;
        font-weight: 500;
        color: #f4f4f5;
        margin-bottom: 2px;
    }

    .hm-match-meta {
        font-size: 0.75rem;
        color: #52525b;
        letter-spacing: 0.02em;
    }

    .hm-match-reason {
        font-size: 0.78rem;
        color: #71717a;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #1c1c1f;
        font-style: italic;
    }

    /* ── AVATAR ─────────────────────────────── */
    .hm-avatar {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: #18181b;
        border: 1px solid #27272a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Playfair Display', serif;
        font-size: 0.95rem;
        color: #71717a;
        flex-shrink: 0;
    }

    /* ── SCORES ─────────────────────────────── */
    .hm-score {
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 11px;
        border-radius: 999px;
        white-space: nowrap;
        letter-spacing: 0.02em;
    }

    .hm-score-high {
        background: rgba(16,185,129,0.08);
        color: #34d399;
        border: 1px solid rgba(16,185,129,0.15);
    }

    .hm-score-mid {
        background: rgba(161,161,170,0.08);
        color: #a1a1aa;
        border: 1px solid rgba(161,161,170,0.12);
    }

    .hm-score-low {
        background: rgba(239,68,68,0.08);
        color: #f87171;
        border: 1px solid rgba(239,68,68,0.12);
    }

    /* ── TAGS ───────────────────────────────── */
    .hm-tag {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.04em;
        padding: 3px 10px;
        border-radius: 999px;
        background: #18181b;
        border: 1px solid #27272a;
        color: #71717a;
        margin-right: 5px;
        margin-bottom: 5px;
    }

    /* ── PROFILE ────────────────────────────── */
    .hm-profile {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 14px;
        padding: 1.6rem;
        animation: fadeUp 0.6s ease both;
    }

    .hm-profile-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        font-weight: 500;
        color: #f4f4f5;
        margin-bottom: 0.2rem;
    }

    .hm-profile-meta {
        font-size: 0.75rem;
        color: #52525b;
        margin-bottom: 1rem;
        letter-spacing: 0.02em;
    }

    /* ── STRENGTH ───────────────────────────── */
    .hm-strength {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 8px;
        padding: 0.5rem 0.9rem;
        font-size: 0.8rem;
        color: #71717a;
        margin-bottom: 0.5rem;
        font-style: italic;
        font-weight: 300;
        transition: border-color 0.2s;
    }

    .hm-strength:hover { border-color: #3f3f46; }

    /* ── TASK BOARD ─────────────────────────── */
    .hm-task {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.83rem;
        color: #a1a1aa;
        font-weight: 300;
        transition: border-color 0.2s;
        animation: fadeUp 0.4s ease both;
    }

    .hm-task:hover { border-color: #3f3f46; }
    .hm-task-todo { border-left: 2px solid #3f3f46; }
    .hm-task-progress { border-left: 2px solid #a1a1aa; }
    .hm-task-done {
        border-left: 2px solid #27272a;
        opacity: 0.35;
        text-decoration: line-through;
    }

    /* ── CHAT ───────────────────────────────── */
    .hm-chat-me {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 14px 14px 4px 14px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0 0.4rem 20%;
        font-size: 0.83rem;
        color: #d4d4d8;
        font-weight: 300;
        animation: fadeUp 0.4s ease both;
    }

    .hm-chat-other {
        background: #111113;
        border: 1px solid #1c1c1f;
        border-radius: 14px 14px 14px 4px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 20% 0.4rem 0;
        font-size: 0.83rem;
        color: #71717a;
        font-weight: 300;
        animation: fadeUp 0.4s ease both;
    }

    .hm-chat-sender {
        font-size: 0.68rem;
        color: #3f3f46;
        margin-bottom: 4px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── BUTTONS ────────────────────────────── */
    .stButton > button {
        background: #f4f4f5 !important;
        color: #09090b !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.6rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.03em !important;
        transition: background 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #e4e4e7 !important;
    }

    /* ── INPUTS ─────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #111113 !important;
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
        color: #d4d4d8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 300 !important;
        transition: border-color 0.2s !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #52525b !important;
        box-shadow: none !important;
    }

    .stTextInput label, .stTextArea label {
        color: #52525b !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    /* ── SELECT ─────────────────────────────── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: #111113 !important;
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
        color: #d4d4d8 !important;
    }

    /* ── TABS ───────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: #111113 !important;
        border: 1px solid #1c1c1f !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 7px !important;
        color: #52525b !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.83rem !important;
    }

    .stTabs [aria-selected="true"] {
        background: #1c1c1f !important;
        color: #f4f4f5 !important;
    }

    /* ── RADIO ──────────────────────────────── */
    .stRadio label {
        background: #111113 !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        color: #71717a !important;
        font-size: 0.83rem !important;
        transition: border-color 0.2s !important;
    }

    /* ── PROGRESS ───────────────────────────── */
    .stProgress > div > div > div {
        background: #d4d4d8 !important;
        border-radius: 999px !important;
    }

    .stProgress > div > div {
        background: #1c1c1f !important;
        border-radius: 999px !important;
    }

    /* ── ALERTS ─────────────────────────────── */
    .stSuccess > div {
        background: rgba(16,185,129,0.05) !important;
        border: 1px solid rgba(16,185,129,0.1) !important;
        border-radius: 10px !important;
        color: #6ee7b7 !important;
    }

    .stError > div {
        background: rgba(239,68,68,0.05) !important;
        border: 1px solid rgba(239,68,68,0.1) !important;
        border-radius: 10px !important;
    }

    /* ── EXPANDER ───────────────────────────── */
    .streamlit-expanderHeader {
        background: #111113 !important;
        border: 1px solid #1c1c1f !important;
        border-radius: 10px !important;
        color: #52525b !important;
        font-size: 0.83rem !important;
    }

    hr {
        border: none !important;
        border-top: 1px solid #1c1c1f !important;
        margin: 2.5rem 0 !important;
    }
    </style>

    /* ── LOADING STATES ─────────────────────── */
    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .hm-skeleton {
        background: linear-gradient(
            90deg,
            #1c1c1f 25%,
            #27272a 50%,
            #1c1c1f 75%
        );
        background-size: 400px 100%;
        animation: shimmer 1.4s ease infinite;
        border-radius: 8px;
    }

    .hm-spinner {
        width: 18px;
        height: 18px;
        border: 2px solid #27272a;
        border-top-color: #d4d4d8;
        border-radius: 50%;
        animation: spin 0.7s linear infinite;
        display: inline-block;
    }

    .hm-loading-text {
        animation: pulse 1.5s ease infinite;
        color: #52525b;
        font-size: 0.82rem;
        font-weight: 300;
        letter-spacing: 0.04em;
    }

    .hm-page-enter {
        animation: fadeInUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
    }
    """