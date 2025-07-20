from firebase_config import db
from datetime import datetime

def save_quiz_attempt(user_id, user_name, user_email, attempt):
    # 🔒 Validate input
    if not all([user_id, user_name, user_email]):
        raise ValueError("One or more user fields are missing.")

    if not attempt or not attempt.get("questions") or not attempt.get("answers"):
        raise ValueError("Missing quiz data — questions or answers are empty.")

    # 🕒 Parse or set timestamp
    attempted_at = attempt.get("attempted_at")
    if isinstance(attempted_at, str):
        attempted_at = datetime.fromisoformat(attempted_at)
    elif attempted_at is None:
        attempted_at = datetime.now()


    # 🧠 Save structured data — no stringification
    doc_ref = db.collection("quiz_attempts").document()
    doc_ref.set({
        "user_id": user_id,
        "user_name": user_name,
        "user_email": user_email,
        "topic": attempt.get("topic", "Unknown Topic"),
        "type": attempt.get("type", "Multiple Choice"),
        "difficulty": attempt.get("difficulty", "Unknown"),
        "score": attempt.get("score", "0/0"),
        "percentage": attempt.get("percentage", "0%"),
        "questions": attempt["questions"],  # ✅ keep raw list[dict]
        "answers": {str(k): v for k, v in attempt["answers"].items()},  # ✅ keys as str
        "attempted_at": attempted_at
    })

def get_attempts_for_user(user_id):
    if not user_id:
        return []

    docs = db.collection("quiz_attempts") \
             .where("user_id", "==", user_id) \
             .order_by("attempted_at", direction="DESCENDING") \
             .stream()

    attempts = []
    for doc in docs:
        data = doc.to_dict()
        attempts.append({
            "topic": data.get("topic"),
            "type": data.get("type"),
            "difficulty": data.get("difficulty"),
            "score": data.get("score"),
            "percentage": data.get("percentage"),
            "questions": data.get("questions"),
            "answers": data.get("answers"),
            "attempted_at": data.get("attempted_at")
        })

    return attempts
