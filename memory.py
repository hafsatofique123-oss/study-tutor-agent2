# =========================================================
# STUDY TUTOR MEMORY
# =========================================================

def create_memory():
    """
    Create an empty memory structure for the Study Tutor.
    """

    return {
        "subject": "",
        "level": "",
        "learning_goal": "",
        "topics_covered": [],
        "weak_topics": [],
        "completed_topics": [],
        "recent_questions": [],
    }


# =========================================================
# UPDATE MEMORY
# =========================================================

def update_memory(
    memory,
    subject=None,
    level=None,
    learning_goal=None,
    topic=None,
    weak_topic=None,
    completed_topic=None,
    question=None,
):
    """
    Update the student's learning memory.
    """

    if subject:
        memory["subject"] = subject

    if level:
        memory["level"] = level

    if learning_goal:
        memory["learning_goal"] = learning_goal

    if topic and topic not in memory["topics_covered"]:
        memory["topics_covered"].append(topic)

    if weak_topic and weak_topic not in memory["weak_topics"]:
        memory["weak_topics"].append(weak_topic)

    if completed_topic and completed_topic not in memory["completed_topics"]:
        memory["completed_topics"].append(completed_topic)

    if question:
        memory["recent_questions"].append(question)

        # Keep only the latest 10 questions
        memory["recent_questions"] = memory["recent_questions"][-10:]

    return memory


# =========================================================
# MEMORY SUMMARY
# =========================================================

def get_memory_summary(memory):
    """
    Convert the student's memory into a readable summary
    that can be provided to the AI Tutor.
    """

    subject = memory.get("subject", "Not specified")
    level = memory.get("level", "Not specified")
    learning_goal = memory.get(
        "learning_goal",
        "Not specified",
    )

    topics_covered = memory.get(
        "topics_covered",
        [],
    )

    weak_topics = memory.get(
        "weak_topics",
        [],
    )

    completed_topics = memory.get(
        "completed_topics",
        [],
    )

    recent_questions = memory.get(
        "recent_questions",
        [],
    )

    summary = f"""
STUDENT MEMORY
==============

Subject:
{subject}

Learning Level:
{level}

Learning Goal:
{learning_goal}

Topics Covered:
{", ".join(topics_covered) if topics_covered else "None yet"}

Weak Topics:
{", ".join(weak_topics) if weak_topics else "None identified yet"}

Completed Topics:
{", ".join(completed_topics) if completed_topics else "None yet"}

Recent Questions:
{chr(10).join(f"- {q}" for q in recent_questions)
if recent_questions else "None yet"}
"""

    return summary.strip()
