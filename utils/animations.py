
def load_animations():
    return """
    <style>

    /* Animated gradient blobs */
    .blob {
        position: fixed;
        border-radius: 999px;
        filter: blur(90px);
        opacity: 0.18;
        z-index: -1;
        animation: floatBlob 14s ease-in-out infinite;
    }

    .blob-1 {
        width: 320px;
        height: 320px;
        background: #7c3aed;
        top: -80px;
        left: -60px;
    }

    .blob-2 {
        width: 280px;
        height: 280px;
        background: #2563eb;
        top: 300px;
        right: -80px;
        animation-delay: 2s;
    }

    .blob-3 {
        width: 240px;
        height: 240px;
        background: #4f46e5;
        bottom: -80px;
        left: 35%;
        animation-delay: 4s;
    }

    @keyframes floatBlob {
        0% {
            transform: translateY(0px) translateX(0px);
        }

        50% {
            transform: translateY(-30px) translateX(20px);
        }

        100% {
            transform: translateY(0px) translateX(0px);
        }
    }

    /* Premium buttons */
    .stButton > button {
        background: linear-gradient(
            135deg,
            #7c3aed,
            #4f46e5
        ) !important;

        border: none !important;
        border-radius: 14px !important;
        color: white !important;
        font-weight: 600 !important;

        transition:
            transform .25s ease,
            box-shadow .25s ease !important;

        height: 50px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 30px rgba(124,58,237,.35);
    }

    /* Premium cards */
    .glass-card {
        background: rgba(17,17,19,.72);
        backdrop-filter: blur(18px);

        border: 1px solid rgba(255,255,255,.06);

        transition:
            transform .3s ease,
            border-color .3s ease;
    }

    .glass-card:hover {
        transform: translateY(-6px);

        border-color:
            rgba(124,58,237,.5);
    }

    /* Hero title gradient */
    .hero-gradient {
        background: linear-gradient(
            135deg,
            #ffffff,
            #a78bfa,
            #60a5fa
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    </style>
    """

