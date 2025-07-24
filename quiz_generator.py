
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
        You are a professional quiz generator.
        
        🎯 TASK:
        Generate exactly {num_questions} multiple-choice questions on the topic "{topic}".
        Each question should:
        - Match the type: {qtype}
        - Match the difficulty: {difficulty}
        - Be clear, accurate, and not vague
        - Include exactly 4 diverse and logical answer options
        
        ✅ REQUIREMENTS:
        - The correct answer **must be one of the 4 options**
        - Provide a brief and factual explanation (max 30 words)
        - Ensure technical correctness (no hallucinations or generalizations)
        - No duplicates. No jokes. No trivia. No pop culture.
        - Focus only on the topic: **{topic}**
        
        🧠 FORMAT (Strict JSON):
        [
          {{
            "question": "Your question here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Exact match of one of the options above",
            "explanation": "Why this answer is correct"
          }},
          ...
        ]
        
        ⚠️ CRITICAL:
        - Return only raw JSON (no markdown, no text)
        - Validate JSON before submitting
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
