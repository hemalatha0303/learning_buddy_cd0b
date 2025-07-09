'''import streamlit as st
import os
import json
import re
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# ✅ Securely set OpenAI key (you can also use a .env file)
OPENAI_API_KEY = "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"  # Replace with your valid OpenAI key starting with sk-
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ✅ Initialize LLM (adjust model name if needed)
llm = ChatOpenAI(
    temperature=0.2,
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name="gpt-4o-mini"  # Use a reliable model; avoid unsupported like gpt-4o-mini for now
)

st.title("📚 Learning Buddy - Quiz Generator")

# Step 1: User Inputs
topic = st.text_input("Enter a Math Topic (e.g., Algebra, Calculus, etc.)")
difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=3)

# Session State Initialization
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "show_answers" not in st.session_state:
    st.session_state.show_answers = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# Step 2: Generate Quiz
if st.button("Generate Quiz"):
    st.session_state.quiz_data = None
    st.session_state.show_answers = False
    st.session_state.user_answers = {}

    with st.spinner("Generating questions..."):
        prompt = f"""
            You are a skilled math quiz generator. Generate {num_questions} {difficulty.lower()}-level multiple-choice math questions on the topic: "{topic}".

            Each question must be in the following JSON format:
            {{
            "question": "...",
            "options": ["...", "...", "...", "..."],  # Exactly 4 options
            "correct_answer": "...",                  # Must match one of the options
            "explanation": "..."
            }}

            All questions should be returned inside a valid JSON array like:
            [
            {{
                "question": "...",
                "options": ["...", "...", "...", "..."],
                "correct_answer": "...",
                "explanation": "..."
            }},
            ...
            ]

            Rules:
            - Do not add any commentary or text outside of the JSON.
            - Ensure correct_answer is **identical** to one of the 4 options.
            - Each option should be a full sentence or phrase, not a label like "A" or "B".

            Return only a valid JSON array.
        """

        try:
            response = llm([HumanMessage(content=prompt)], timeout=30)
            content = response.content.strip()

            # ✅ Extract JSON array from LLM output
            json_match = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL)
            #.....json_match = re.search(r"\[\s*{.*}\s*\]", content, re.DOTALL)
            if not json_match:
                raise ValueError("Unable to parse valid quiz JSON. Try reducing difficulty or check formatting.")

            raw_json = json_match.group(0)
            quiz_data = json.loads(raw_json)

            # ✅ Structure validation
            # Validate structure
            for idx, item in enumerate(quiz_data):
                if not all(key in item for key in ["question", "options", "correct_answer", "explanation"]):
                    raise ValueError(f"Missing key in question {idx+1}")
                if not isinstance(item["options"], list) or len(item["options"]) != 4:
                    raise ValueError(f"Question {idx+1} must have exactly 4 options")
                if item["correct_answer"] not in item["options"]:
                    raise ValueError(f"Correct answer not found in options for question {idx+1}")


            st.session_state.quiz_data = quiz_data

        except Exception as e:
            st.error(f"❌ Failed to generate valid quiz questions.\n**Reason:** {str(e)}")
            if 'content' in locals():
                st.code(content, language="json")

# Step 3: Show Questions
if st.session_state.quiz_data:
    st.subheader("📝 Quiz Time!")
    for idx, item in enumerate(st.session_state.quiz_data):
        st.write(f"**Q{idx+1}: {item['question']}**")
        st.session_state.user_answers[idx] = st.radio(
            f"Choose your answer (Q{idx+1})",
            item['options'],
            key=f"q_{idx}",
            index=None 
        )
        st.markdown("---")

    all_answered = all(idx in st.session_state.user_answers for idx in range(len(st.session_state.quiz_data)))
    if st.button("Submit Answers", disabled=not all_answered):
        st.session_state.show_answers = True

# Step 4: Show Results
if st.session_state.show_answers:
    st.subheader("✅ Results")
    score = 0
    total = len(st.session_state.quiz_data)

    for idx, item in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers.get(idx)
        correct = item["correct_answer"]
        explanation = item["explanation"]
        result = "✅ Correct!" if user_ans == correct else "❌ Incorrect"
        if user_ans == correct:
            score += 1

        with st.expander(f"Q{idx+1} Answer & Explanation"):
            st.write(f"**Your Answer:** {user_ans}")
            st.write(f"**Correct Answer:** {correct}")
            st.write(f"**Result:** {result}")
            st.write(f"**Explanation:** {explanation}")

    accuracy = (score / total) * 100
    st.markdown(f"### Your Score: **{score}/{total}** ({accuracy:.2f}%)")

# quiz_generator.py
import os
import re
import json
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
from langchain_together import ChatTogether

load_dotenv()
llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct",
    temperature=0.2,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

def generate_quiz(topic, qtype, difficulty, num_questions):
    prompt = f"""
        You are a skilled quiz generator. Generate {num_questions} {difficulty.lower()} {qtype.lower()} questions on: "{topic}".

        Format:
        [{{
            "question": "...",
            "options": ["...", "...", "...", "..."],
            "correct_answer": "...",
            "explanation": "..."
        }}]
        Return only valid JSON array.
    """
    response = llm([HumanMessage(content=prompt)], timeout=30)
    content = response.content.strip()

    json_match = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL)
    if not json_match:
        raise ValueError("Unable to parse JSON. Try a different input.")

    quiz_data = json.loads(json_match.group(0))
    
    for i, item in enumerate(quiz_data):
        if not all(k in item for k in ["question", "options", "correct_answer", "explanation"]):
            raise ValueError(f"Missing keys in Q{i+1}")
        if len(item["options"]) != 4:
            raise ValueError(f"Q{i+1} must have 4 options")
        if item["correct_answer"] not in item["options"]:
            raise ValueError(f"Correct answer missing in options for Q{i+1}")

    return quiz_data
'''

from langchain.schema import HumanMessage
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os, json

load_dotenv()
llm = ChatTogether(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.2,
    together_api_key=os.getenv("TOGETHER_API_KEY")
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
