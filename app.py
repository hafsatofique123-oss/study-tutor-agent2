import streamlit as st
from pypdf import PdfReader

from agent import create_study_tutor, run_study_tutor
from memory import (
    create_memory,
    update_memory,
    get_memory_summary,
)
from tools import (
    create_quiz,
    create_study_plan,
    explain_topic,
    analyze_weak_topic,
)
from rag import build_rag_index, search_documents


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
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(0, 191, 255, 0.13),
                transparent 30%
            ),
            radial-gradient(
                circle at bottom right,
                rgba(0, 102, 255, 0.12),
                transparent 30%
            ),
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
        color: white;
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
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = create_memory()

if "rag_index" not in st.session_state:
    st.session_state.rag_index = None

if "rag_chunks" not in st.session_state:
    st.session_state.rag_chunks = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


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
        height=110,
    )

    st.markdown("---")

    st.markdown("### 📄 Study Material")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        help="PDF is optional. You can use the tutor without uploading a PDF.",
    )

    if uploaded_file is not None:

        if (
            st.session_state.uploaded_file_name
            != uploaded_file.name
        ):

            with st.spinner("📚 Reading your PDF..."):

                try:

                    reader = PdfReader(uploaded_file)

                    page_texts = []

                    for page_number, page in enumerate(
                        reader.pages,
                        start=1,
                    ):

                        text = page.extract_text() or ""

                        if text.strip():

                            page_texts.append(
                                f"\n[PAGE {page_number}]\n{text}"
                            )

                    complete_text = "\n".join(page_texts)

                    if not complete_text.strip():

                        st.error(
                            "I could not extract readable text from this PDF."
                        )

                    else:

                        index, chunks = build_rag_index(
                            complete_text
                        )

                        st.session_state.rag_index = index
                        st.session_state.rag_chunks = chunks
                        st.session_state.uploaded_file_name = (
                            uploaded_file.name
                        )

                        st.success(
                            f"✅ {uploaded_file.name} loaded"
                        )

                        st.caption(
                            f"Pages: {len(reader.pages)}"
                        )

                        st.caption(
                            f"Knowledge chunks: {len(chunks)}"
                        )

                except Exception as error:

                    st.error(
                        f"Could not process the PDF: {error}"
                    )

    elif st.session_state.uploaded_file_name:

        st.session_state.rag_index = None
        st.session_state.rag_chunks = []
        st.session_state.uploaded_file_name = None

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.session_state.memory = create_memory()

        st.rerun()

    st.markdown(
        """
        <div class="status-box">
            <strong>🤖 AI Study Tutor</strong><br>
            Learn with personalized explanations,
            quizzes, study plans, memory and your own notes.
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
    '<div class="subtitle">'
    'Your personal AI learning assistant'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# INTRODUCTION
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="info-card">

        <h3>✨ Welcome to your AI Study Tutor</h3>

        <p>
        Enter your subject, select your learning level,
        describe your learning goal and start asking questions.
        You can also upload your own study PDF.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# DISPLAY CHAT HISTORY
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
    # VALIDATION
    # -----------------------------------------------------

    if not subject:

        st.warning(
            "📚 Please enter your subject first."
        )

        st.stop()

    if not learning_goal:

        st.warning(
            "🚀 Please enter your learning goal first."
        )

        st.stop()

    # -----------------------------------------------------
    # CREATE / UPDATE MEMORY
    # -----------------------------------------------------

    st.session_state.memory = update_memory(
        st.session_state.memory,
        subject=subject,
        level=level,
        learning_goal=learning_goal,
        question=user_prompt,
    )

    # -----------------------------------------------------
    # SAVE USER MESSAGE
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
    # CREATE STUDY TUTOR
    # -----------------------------------------------------

    try:

        tutor = create_study_tutor(
            subject=subject,
            level=level,
            learning_goal=learning_goal,
        )

    except Exception as error:

        st.error(
            f"Could not initialize the AI Tutor: {error}"
        )

        st.stop()

    # -----------------------------------------------------
    # MEMORY CONTEXT
    # -----------------------------------------------------

    memory_context = get_memory_summary(
        st.session_state.memory
    )

    # -----------------------------------------------------
    # DETECT SPECIAL TOOL REQUESTS
    # -----------------------------------------------------

    prompt_lower = user_prompt.lower()

    tool_instruction = ""

    # Quiz
    if (
        "quiz" in prompt_lower
        or "mcq" in prompt_lower
        or "test me" in prompt_lower
    ):

        tool_instruction = create_quiz(
            topic=subject,
            level=level,
            number_of_questions=5,
        )

    # Study plan
    elif (
        "study plan" in prompt_lower
        or "learning plan" in prompt_lower
        or "schedule" in prompt_lower
    ):

        tool_instruction = create_study_plan(
            subject=subject,
            topic=user_prompt,
            level=level,
            learning_goal=learning_goal,
            duration_days=7,
        )

    # Explain
    elif (
        "explain" in prompt_lower
        or "what is" in prompt_lower
        or "what are" in prompt_lower
        or "how does" in prompt_lower
    ):

        tool_instruction = explain_topic(
            topic=user_prompt,
            level=level,
        )

    # Weak topic
    elif (
        "wrong" in prompt_lower
        or "mistake" in prompt_lower
        or "weak" in prompt_lower
        or "check my answer" in prompt_lower
    ):

        tool_instruction = analyze_weak_topic(
            topic=subject,
            student_answer=user_prompt,
        )

    # -----------------------------------------------------
    # PDF / RAG SEARCH
    # -----------------------------------------------------

    retrieved_context = ""

    if (
        st.session_state.rag_index is not None
        and st.session_state.rag_chunks
    ):

        with st.spinner("📚 Searching your study material..."):

            try:

                results = search_documents(
                    question=user_prompt,
                    chunks=st.session_state.rag_chunks,
                    index=st.session_state.rag_index,
                    top_k=5,
                )

                if results:

                    context_parts = []

                    for result in results:

                        context_parts.append(
                            result["text"]
                        )

                    retrieved_context = "\n\n".join(
                        context_parts
                    )

            except Exception as error:

                st.warning(
                    f"PDF search could not be completed: {error}"
                )

    # -----------------------------------------------------
    # BUILD ENHANCED USER CONTEXT
    # -----------------------------------------------------

    enhanced_prompt = f"""
STUDENT MEMORY
--------------
{memory_context}

"""

    if tool_instruction:

        enhanced_prompt += f"""
SPECIAL STUDY TOOL INSTRUCTION
------------------------------
{tool_instruction}

"""

    if retrieved_context:

        enhanced_prompt += f"""
STUDENT'S UPLOADED STUDY MATERIAL
---------------------------------
The following information was retrieved from the student's
uploaded PDF.

Use this material when it is relevant to the question.

IMPORTANT:
- Do not invent information from the PDF.
- If the answer is not available in the retrieved material,
  clearly say that it is not found in the uploaded material.
- The PDF contains page markers such as [PAGE 1], [PAGE 2], etc.
- Mention the relevant page when possible.

PDF SOURCE:
{st.session_state.uploaded_file_name}

RETRIEVED CONTENT:
{retrieved_context}

"""

    enhanced_prompt += f"""
CURRENT STUDENT QUESTION
------------------------
{user_prompt}
"""

    # -----------------------------------------------------
    # BUILD CONVERSATION
    # -----------------------------------------------------

    conversation = []

    # Add previous conversation
    for message in st.session_state.messages[:-1]:

        conversation.append(
            {
                "role": message["role"],
                "content": message["content"],
            }
        )

    # Add enhanced current request
    conversation.append(
        {
            "role": "user",
            "content": enhanced_prompt,
        }
    )

    # -----------------------------------------------------
    # GENERATE RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Your AI Tutor is thinking..."
        ):

            try:

                assistant_response = run_study_tutor(
                    tutor=tutor,
                    conversation=conversation,
                )

            except Exception as error:

                assistant_response = (
                    "I couldn't generate a response right now.\n\n"
                    f"Error: {error}"
                )

        st.markdown(assistant_response)

    # -----------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )
