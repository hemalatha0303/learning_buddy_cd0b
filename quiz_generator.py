import openai
import json

def generate_quiz(topic, qtype, difficulty, num_questions):
    prompt = f"""
You are a master quiz generator AI, trained to create structured, challenging, and unique multiple-choice questions.

Generate {num_questions} '{qtype}' type questions on the topic "{topic}" with '{difficulty}' difficulty level.

Each question must:
- Be clearly phrased and relevant to the topic.
- Contain exactly **4 distinct answer options** (A, B, C, D).
- Specify the correct answer explicitly using the **option letter**, not the text.

⚠️ Output ONLY valid JSON. Do NOT include any explanation or extra commentary.

Use this **exact format**:

[
  {{
    "question": "Your question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "A"
  }},
  ...
]
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    content = response.choices[0].message.content.strip()

    try:
        # Attempt direct parsing
        quiz = json.loads(content)
        return quiz
    except json.JSONDecodeError:
        # Auto-repair malformed JSON (e.g., with explanation text or trailing text)
        try:
            json_start = content.find("[")
            json_end = content.rfind("]") + 1
            fixed_json = content[json_start:json_end]
            quiz = json.loads(fixed_json)
            return quiz
        except Exception as e:
            raise ValueError("❌ Quiz generation failed: Invalid JSON returned by LLM.") from e
