# =========================================================
# STUDY TUTOR TOOLS
# =========================================================

# These tools provide structured learning features
# for the AI Study Tutor.


# =========================================================
# QUIZ TOOL
# =========================================================

def create_quiz(topic, level, number_of_questions=5):
    """
    Create instructions for generating a quiz.

    The actual quiz generation will be handled by the
    Groq LLM.
    """

    return f"""
Create a quiz for the student.

Topic:
{topic}

Learning Level:
{level}

Number of Questions:
{number_of_questions}

Requirements:
- Make the questions suitable for the student's level.
- Include a mixture of conceptual and practical questions.
- Clearly number each question.
- Include multiple-choice options where appropriate.
- Provide the correct answer after each question.
- Add a short explanation for the answer.
"""


# =========================================================
# STUDY PLAN TOOL
# =========================================================

def create_study_plan(
    subject,
    topic,
    level,
    learning_goal,
    duration_days=7,
):
    """
    Create instructions for generating a personalized
    study plan.
    """

    return f"""
Create a personalized study plan.

Subject:
{subject}

Topic:
{topic}

Learning Level:
{level}

Learning Goal:
{learning_goal}

Duration:
{duration_days} days

Requirements:
- Divide the learning into manageable daily tasks.
- Start from the appropriate difficulty level.
- Include theory and practical learning.
- Include revision.
- Include practice questions.
- Include a final review.
- Keep the plan realistic and easy to follow.
"""


# =========================================================
# TOPIC EXPLANATION TOOL
# =========================================================

def explain_topic(topic, level):
    """
    Create instructions for explaining a topic.
    """

    return f"""
Explain the following topic to a student.

Topic:
{topic}

Learning Level:
{level}

Requirements:
- Start with a simple definition.
- Explain the concept step by step.
- Use a simple real-world example.
- Mention important points.
- Avoid unnecessary complexity.
- End with a short practice question.
"""


# =========================================================
# WEAK TOPIC TOOL
# =========================================================

def analyze_weak_topic(topic, student_answer):
    """
    Create instructions for analyzing a student's answer
    and identifying possible weak areas.
    """

    return f"""
Analyze the student's answer.

Topic:
{topic}

Student Answer:
{student_answer}

Requirements:
- Identify what the student understood correctly.
- Identify mistakes or missing concepts.
- Identify the likely weak area.
- Explain how the student can improve.
- Give one short practice question.
"""


# =========================================================
# WEB SEARCH TOOL PLACEHOLDER
# =========================================================

def create_web_search_query(question):
    """
    Prepare a clean search query for future web search.

    The actual web search integration will be connected
    later without adding unnecessary dependencies.
    """

    return question.strip()


# =========================================================
# TOOL LIST
# =========================================================

def get_available_tools():
    """
    Return the names of all available Study Tutor tools.
    """

    return [
        "quiz_generator",
        "study_plan_generator",
        "topic_explainer",
        "weak_topic_analyzer",
        "web_search",
    ]
