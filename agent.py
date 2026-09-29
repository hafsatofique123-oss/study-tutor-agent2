import os

from groq import Groq


# =========================================================
# GROQ API KEY
# =========================================================

def get_api_key():
    """
    Get the Groq API key.

    First checks the normal environment variable.
    Then checks Streamlit Secrets if available.
    """

    api_key = os.environ.get("GROQ_API_KEY")

    if api_key:
        return api_key

    # Streamlit Cloud Secrets fallback
    try:
        import streamlit as st

        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]

    except Exception:
        pass

    return None


# =========================================================
# GROQ CLIENT
# =========================================================

def get_groq_client():
    """
    Create and return the Groq client.
    """

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured. "
            "Please add GROQ_API_KEY to Streamlit Secrets."
        )

    return Groq(
        api_key=api_key
    )


# =========================================================
# STUDY TUTOR SYSTEM PROMPT
# =========================================================

def build_system_prompt(
    subject,
    level,
    learning_goal,
):
    """
    Create the system instructions for the Study Tutor.
    """

    return f"""
You are an AI Study Tutor.

Your main purpose is to help the student understand
and learn their chosen subject effectively.

STUDENT PROFILE
---------------

Subject:
{subject}

Learning Level:
{level}

Learning Goal:
{learning_goal}


TEACHING RULES
--------------

1. Explain concepts according to the student's learning level.

2. Use simple and clear language.

3. Break difficult concepts into smaller steps.

4. Give practical examples when useful.

5. Avoid unnecessary technical language.

6. If the student is confused, explain the concept
   in an easier way.

7. Encourage active learning.

8. Ask a short follow-up question when it helps
   the learning process.

9. If the student requests a study plan,
   create a realistic plan.

10. If the student requests a quiz,
    create questions suitable for the student's level.

11. Stay focused on education and the student's
    learning goal.

12. Never pretend that you used a tool, document,
    website, or source that you did not actually use.

13. When information from the student's uploaded
    study material is provided, use it when relevant.

14. If the uploaded study material does not contain
    the requested information, clearly say so.

15. Be encouraging but do not give unnecessary
    or overly long answers.
"""


# =========================================================
# CREATE STUDY TUTOR
# =========================================================

def create_study_tutor(
    subject,
    level,
    learning_goal,
):
    """
    Create the Study Tutor configuration.
    """

    client = get_groq_client()

    system_prompt = build_system_prompt(
        subject=subject,
        level=level,
        learning_goal=learning_goal,
    )

    return {
        "client": client,
        "system_prompt": system_prompt,
        "model": "openai/gpt-oss-120b",
    }


# =========================================================
# RUN STUDY TUTOR
# =========================================================

def run_study_tutor(
    tutor,
    conversation,
):
    """
    Send the conversation to Groq
    and return the tutor response.
    """

    messages = [
        {
            "role": "system",
            "content": tutor["system_prompt"],
        }
    ]

    messages.extend(conversation)

    response = tutor["client"].chat.completions.create(
        model=tutor["model"],
        messages=messages,
        temperature=0.4,
    )

    return response.choices[0].message.content
