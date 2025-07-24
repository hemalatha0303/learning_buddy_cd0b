
import os
import json
import streamlit as st
from langchain.schema import HumanMessage
from langchain_together import ChatTogether
import random

# Fix: Dummy key to satisfy OpenAI dependency
os.environ["OPENAI_API_KEY"] = st.secrets["together"]["TOGETHER_API_KEY"]

llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.2,
    together_api_key=st.secrets["together"]["TOGETHER_API_KEY"]
)

def generate_quiz(topic, qtype, difficulty, num_questions):
    prompt = f"""
        You are an expert quiz generator. Return ONLY a **valid JSON array** — no markdown, no comments, no extra text.

        🎯 TASK:
        Generate exactly {num_questions} multiple-choice quiz questions (type: {qtype}, difficulty: {difficulty}) on the topic: "{topic}".

        🧠 RULES:
        - Each question must be clear, factually correct, and unambiguous.
        - Provide 4 diverse and plausible options per question.
        - Ensure the correct_answer is 100% present in the options.
        - Add a concise explanation that justifies the correct answer.
        - Avoid duplicates or vague phrasing.

        📦 JSON FORMAT (strictly):
        [
        {{
            "question": "What is ...?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option B",
            "explanation": "Explanation for why Option B is correct."
        }},
        ...
        ]

        ⚠️ DO NOT return any preamble, markdown, or notes — only a valid JSON array.
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

        # 🛡️ Ensure 4 options
        if len(item["options"]) != 4:
            raise ValueError(f"Q{i+1} must have 4 options")

        # ✅ Ensure correct answer is in options
        if item["correct_answer"] not in item["options"]:
            # Replace last option with correct one if needed
            item["options"][-1] = item["correct_answer"]
            random.shuffle(item["options"])  # Optional: re-shuffle

    return quiz_data
