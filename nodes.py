from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langgraph.types import interrupt

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3,
    max_tokens=300,
    streaming=True
)


def drafter_node(state):

    prompt = state["prompt"]
    feedback = state.get("feedback")

    if feedback:
        instruction = f"""
Revise the email based on feedback.

Original request:
{prompt}

Feedback:
{feedback}

Return a professional email.
"""
    else:
        instruction = f"""
Write a professional email for this request:

{prompt}
"""

    response = llm.invoke(instruction)

    draft = response.content

    # Pause graph and wait for human decision
    human_input = interrupt(
        {
            "draft": draft,
            "message": "Review the email draft and approve or request changes."
        }
    )

    return {
        "draft": draft,
        "approved": human_input.get("approved"),
        "feedback": human_input.get("feedback"),
    }


def send_node(state):

    print("📧 Email Sent!")

    return state