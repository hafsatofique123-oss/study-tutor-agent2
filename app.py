import os

import streamlit as st
from groq import Groq


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS — MODERN NEON BLUE UI
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(0, 191, 255, 0.12), transparent 30%),
                radial-gradient(circle at bottom right, rgba(0, 102, 255, 0.10), transparent 30%),
                #050b18;
            color: #f5f7ff;
        }

        [data-testid="stSidebar"] {
            background: #071224;
            border-right: 1px solid rgba(0, 191, 255, 0.20);
        }

        .main-title {
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-top: 1rem;
            margin-bottom: 0.2rem;
            color: #ffffff;
            text-shadow: 0 0 20px rgba(0, 191, 255, 0.55);
        }

        .subtitle {
            text-align: center;
            color: #9db5d8;
            font-size: 1.05rem;
            margin-bottom: 2rem;
        }

        .info-card {
            background: rgba(10, 25, 50, 0.75);
            border: 1px solid rgba(0, 191, 255, 0.25);
            border-radius: 18px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 25px rgba(0, 191, 255, 0.06);
        }

        .info-card h3 {
            color: #4ddcff;
            margin-bottom: 0.5rem;
        }

        .info-card p {
            color: #b8c9e6;
            margin-bottom: 0;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 16px;
            border: 1px solid rgba(0, 191, 255, 0.12);
            margin-bottom: 0.7rem;
        }

        .stButton > button {
            width: 100%;
            border-radius: 12px;
            border: 1px solid rgba(0, 191, 255, 0.5);
            background: linear-gradient(
                135deg,
                rgba(0, 191, 255, 0.18),
                rgba(0, 102, 255, 0.18)
            );
            color: white;
            font-weight: 600;
        }

        .stButton > button:hover {
            border-color: #4ddcff;
            box-shadow: 0 0 18px rgba(0, 191, 255, 0.30);
            color: white;
        }

        div[data-testid="stChatInput"] {
            border-color: rgba(0, 191, 255, 0.35);
        }

        .status-box {
            padding: 0.8rem 1rem;
            border-radius: 12px;
            background: rgba(0, 191, 255, 0.08);
            border: 1px solid rgba(0, 191, 255, 0.18);
            color: #bdefff;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GROQ CLIENT
# =========================================================

def get_groq_client():
    """Create and return the Groq client."""

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 🎓 Study Settings")

    subject = st.text_input(
        "📚 Subject",
        placeholder="e.g. Python, AI, Law, Biology",
    )

    level = st.selectbox(
        "🎯 Learning Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    learning_goal = st.text_area(
        "🚀 Learning Goal",
        placeholder="What do you want to learn or achieve?",
        height=120,
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="status-box">
            <strong>AI Tutor</strong><br>
            Your personalized learning assistant.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎓 AI Study Tutor</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Your personal AI learning assistant</div>',
    unsafe_allow_html=True,
)


# =========================================================
# INTRODUCTION CARD
# =========================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="info-card">
            <h3>✨ Welcome to your AI Study Tutor</h3>
            <p>
                Enter your subject, choose your learning level, describe your goal,
                and ask me anything you want to learn.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# DISPLAY PREVIOUS CHAT
# =========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_prompt = st.chat_input(
    "💬 Ask your Study Tutor something..."
)


if user_prompt:

    # -----------------------------------------------------
    # Validate basic user information
    # -----------------------------------------------------

    if not subject:
        st.warning("Please enter a subject from the sidebar first.")
        st.stop()

    if not learning_goal:
        st.warning("Please enter your learning goal from the sidebar first.")
        st.stop()

    # -----------------------------------------------------
    # Get Groq client
    # -----------------------------------------------------

    client = get_groq_client()

    if client is None:
        st.error(
            "GROQ_API_KEY is not configured. "
            "Please add GROQ_API_KEY to your Streamlit Secrets."
        )
        st.stop()

    # -----------------------------------------------------
    # Save user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # -----------------------------------------------------
    # System instructions for the tutor
    # -----------------------------------------------------

    system_prompt = f"""
You are an AI Study Tutor.

Your job is to help the student learn clearly and effectively.

Student information:
- Subject: {subject}
- Learning level: {level}
- Learning goal: {learning_goal}

Teaching rules:
1. Explain concepts according to the student's learning level.
2. Use simple and clear language.
3. Break difficult concepts into smaller steps.
4. Give examples when useful.
5. Do not overwhelm the student with unnecessary information.
6. If the student seems confused, explain the concept in an easier way.
7. Encourage active learning by asking short follow-up questions when appropriate.
8. If the student asks for a study plan, create a practical plan based on their goal.
9. If the student asks for a quiz, create questions suitable for their level.
10. Stay focused on helping the student learn.
"""

    # -----------------------------------------------------
    # Prepare conversation
    # -----------------------------------------------------

    api_messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    for message in st.session_state.messages:
        api_messages.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    # -----------------------------------------------------
    # Generate AI response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🤖 Your AI Tutor is thinking..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=api_messages,
                    temperature=0.4,
                )

                assistant_response = response.choices[0].message.content

            except Exception as error:
                assistant_response = (
                    "I couldn't generate a response right now.\n\n"
                    f"Error: {error}"
                )

        st.markdown(assistant_response)

    # -----------------------------------------------------
    # Save assistant response
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )
