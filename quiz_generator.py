
import os
import json
import streamlit as st
from langchain.schema import HumanMessage
from langchain_together import ChatTogether

# ✅ SAFE ACCESS TO secrets
TOGETHER_KEY = st.secrets.get("together", {}).get("TOGETHER_API_KEY", "")
os.environ["OPENAI_API_KEY"] = TOGETHER_KEY
llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.2,
    together_api_key=st.secrets["together"]["TOGETHER_API_KEY"]
)

def generate_quiz(topic, qtype, difficulty, num_questions):
    prompt = f"""
    You are a quiz generator bot. ONLY return valid JSON array — no text or markdown.

    Generate {num_questions} {difficulty.lower()} {qtype.lower()} questions on "{topic}". Format:

    [
    {{
        "question": "...",
        "options": ["...", "...", "...", "..."],
        "correct_answer": "...",
        "explanation": "..."
    }},
    ...
    ]

    Only return a pure JSON array. No explanation, no notes, no markdown. Only output JSON.
    """

    response = llm.invoke([HumanMessage(content=prompt)], config={"timeout": 30})
    content = response.content.strip()

    try:
        quiz_data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON returned by LLM.")

    for i, item in enumerate(quiz_data):
        if not all(k in item for k in ["question", "options", "correct_answer", "explanation"]):
            raise ValueError(f"Missing keys in Q{i+1}")
        if len(item["options"]) != 4:
            raise ValueError(f"Q{i+1} must have 4 options")
        if item["correct_answer"] not in item["options"]:
            raise ValueError(f"Correct answer not in options for Q{i+1}")

    return quiz_data
