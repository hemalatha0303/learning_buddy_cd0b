
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
    You are an expert quiz generator for programming and computer science.
    
    🎯 OBJECTIVE:
    Generate exactly {num_questions} multiple-choice questions on "{topic}" for {difficulty} level.
    
    📌 QUESTION TYPE: {qtype}
    
    Each question must:
    - Be unique, technically accurate, and clearly worded.
    - Include 4 answer choices (one correct).
    - Include explanation for the correct answer.
    
    ⚠️ FORMAT:
    Return ONLY a valid JSON array like:
    [
      {{
        "question": "What is ...?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "B",
        "explanation": "B is correct because..."
      }},
      ...
    ]
    No markdown, no extra text.
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
