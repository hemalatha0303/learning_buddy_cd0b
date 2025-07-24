import os
import json
import streamlit as st
import random
from langchain.schema import HumanMessage
from langchain_together import ChatTogether

# 🔐 Set API Key for Together API
os.environ["OPENAI_API_KEY"] = st.secrets["together"]["TOGETHER_API_KEY"]

# ⚙️ Initialize the Together LLM
llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.2,
    together_api_key=st.secrets["together"]["TOGETHER_API_KEY"]
)

# 🚀 Quiz Generator
def generate_quiz(topic, qtype, difficulty, num_questions):
    prompt = f"""
You are an expert quiz generator for programming and computer science concepts.

🎯 OBJECTIVE:
Generate exactly {num_questions} high-quality multiple-choice questions on the topic: "{topic}", targeting a {difficulty} level audience.

📌 QUESTION TYPE: {qtype}
Each question must:
- Focus on a distinct concept or common misconception.
- Be unambiguous, technically accurate, and clearly worded.
- Avoid overlap between questions.

📌 OPTIONS:
- Provide 4 plausible, non-redundant answer choices.
- Only ONE correct answer (must be one of the options).
- Use realistic distractors.
- Mix theoretical and code-based questions.

📌 EXPLANATION:
- For each question, include a short explanation for the correct answer.
- Explain why it's right and, briefly, why others are wrong if relevant.

⚠️ FORMAT RULES:
Return ONLY a valid JSON array with this structure:
[
  {{
    "question": "Your question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Short explanation here."
  }},
  ...
]
Strictly return ONLY JSON. No markdown, titles, quotes, or extra text.
Ensure JSON is fully closed, properly escaped, and parsable.
"""

    # 🧠 Call LLM
    response = llm.invoke([HumanMessage(content=prompt)], config={"timeout": 60})
    content = response.content.strip()

    # 🔧 Postprocess if needed
    try:
        if content.startswith("```") or "```json" in content:
            content = content.split("```")[-2].strip()
        quiz_data = json.loads(content)
    except Exception:
        raise ValueError("❌ Quiz generation failed: Invalid JSON returned by LLM.")

    # 🔍 Validate Structure
    for i, item in enumerate(quiz_data):
        required_keys = {"question", "options", "correct_answer", "explanation"}
        if not required_keys.issubset(item):
            raise ValueError(f"❌ Q{i+1} missing keys: {required_keys - set(item.keys())}")

        if len(item["options"]) != 4:
            raise ValueError(f"❌ Q{i+1} must have 4 options")

        if item["correct_answer"] not in item["options"]:
            # Auto-correct answer placement
            item["options"][-1] = item["correct_answer"]
            random.shuffle(item["options"])

    return quiz_data
