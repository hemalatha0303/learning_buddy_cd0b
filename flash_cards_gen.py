# flash_cards_gen.py
import json5
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
    
    1. If the request includes a **broad concept or topic** (like "Machine Learning models", "Cloud Computing", "Software Development Life Cycle"), respond using a **mind map** with main node and multiple rich subtopics (with **in-depth explanations**, **examples**, and **historical or real-world context** where appropriate). Each subtopic must be at least 3-5 sentences, and cover **nuances, impacts, and key facts**. You must extract and include **as many relevant subtopics as needed**.
    
    2. If the request is a **direct question or small prompt** (like "Tell me a moral story", "What is Python?", or "Explain AI vs ML"), return **just one flashcard** with **a comprehensive, multi-paragraph answer**. Be **detailed, educational, and thorough**.
    
    Important:
    - If the user says “What are the types of ___” or “List types of ___”, treat it as a topic for a **mind map**.
    - Never give minimal output. Always expand based on user input.
    
    Include these fields:
    - "question": restate the user's prompt.
    - "answer": a rich, clear, multi-paragraph response that fully educates the reader.
    - "summary": (optional) short 1-line key idea.
    
    User Request:
    {text}
    
    Return JSON in one of the following formats:
    
    ### For mind-map:
    [
      {{
        "node": "Main Concept",
        "content": "Provide a strong, paragraph-length overview of the topic, setting context.",
        "children": [
          {{
            "node": "Subtopic",
            "content": "3–6 sentence detailed explanation, including examples, insights, data, or impact. Go deep and be comprehensive.",
            "summary": "optional short summary"
          }},
          ...
        ]
      }}
    ]
    
    ### For single flashcard:
    [
      {{
        "question": "User question rephrased",
        "answer": "Write a detailed, multi-paragraph educational explanation covering all aspects of the question, including examples and implications.",
        "summary": "optional short summary"
      }}
    ]
    """


    # 🔁 Call the LLM
    content = FlashcardLLMRouter.generate(prompt)

    # 🔍 Extract JSON list
    match = re.search(r"\[.*\]", content, re.DOTALL)
    if not match:
        print("LLM raw content:", content)
        raise ValueError("⚠️ Failed to parse PromptSnaps from LLM response.")
    try:
        cards = json5.loads(match.group(0))
    except Exception as e:
        print("Matched JSON string:", match.group(0))  # 🛠️ Debug print
        raise ValueError(f"⚠️ JSON decoding failed: {e}")

    if not isinstance(cards, list) or not cards:
        raise ValueError("⚠️ PromptSnap response must be a non-empty list.")

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
        raise ValueError("Unrecognized PromptSnap format.")

    return validated_cards
