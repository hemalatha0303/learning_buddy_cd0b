# flash_cards_gen.py
import json5 as json
import re
from llm_router import FlashcardLLMRouter

def generate_flashcards(text, difficulty, include_summary):
    summary_instruction = (
        " Include a one-line summary if possible."
        if include_summary else ""
    )

    prompt = f"""
    You are an intelligent learning assistant. 
    Based on the user's request below, decide the most helpful format:

    1. If the request includes a **broad concept or topic** (like "Machine Learning models", "Cloud Computing", "Software Development Life Cycle"), respond using a **mind map** with main node and subtopics (with explanations and optional summaries).

    2. If the request is a **direct question or small prompt** (like "Tell me a moral story", "What is Python?", or "Explain AI vs ML"), return **just one flashcard** with detailed explanation.

    Important: If the user says “What are the types of ___” or “List types of ___”, treat it as a topic for a **mind map**, not a single answer.

    Include these fields:
    - "question": restate the user's prompt.
    - "answer": give a clear, complete, human-friendly response.
    - "summary": (optional) short 1-line key idea.

    User Request:
    {text}

    Return JSON in one of the following formats:

    ### For mind-map:
    [
      {{
        "node": "Main Concept",
        "content": "Optional brief intro to topic",
        "children": [
          {{
            "node": "Subtopic",
            "content": "Explanation here",
            "summary": "optional short summary"
          }}
        ]
      }}
    ]

    ### For single flashcard:
    [
      {{
        "question": "User question rephrased",
        "answer": "Your answer here",
        "summary": "optional short summary"
      }}
    ]
    """

    # 🔁 Call the LLM
    content = FlashcardLLMRouter.generate(prompt)

    # 🔍 Extract JSON list
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if not match:
        raise ValueError("⚠️ Failed to parse flashcards from LLM response.")
    try:
        cards = json.loads(match.group(0))
    except Exception as e:
        raise ValueError(f"⚠️ JSON decoding failed: {e}")

    if not isinstance(cards, list) or not cards:
        raise ValueError("⚠️ Flashcard response must be a non-empty list.")

    first = cards[0]

    validated_cards = []

    if "question" in first and "answer" in first:
        # ✅ SINGLE FLASHCARD
        validated_cards.append({
            "question": first["question"],
            "answer": first["answer"],
            "summary": first.get("summary", "")
        })

    elif "node" in first:
        # ✅ MIND MAP
        node = {
            "node": first["node"],
            "content": first.get("content", ""),
            "children": []
        }

        if "children" in first:
            for child in first["children"]:
                if "node" in child and "content" in child:
                    node["children"].append({
                        "node": child["node"],
                        "content": child["content"],
                        "summary": child.get("summary", "")
                    })

        validated_cards.append(node)

    else:
        raise ValueError("Unrecognized flashcard format.")

    return validated_cards
