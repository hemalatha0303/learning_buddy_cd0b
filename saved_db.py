import json
from datetime import datetime

def save_quiz_attempt(conn, user_email, attempt):
    import json
    from datetime import datetime

    try:
        cursor = conn.cursor()

        # ✅ Create table (only once)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id SERIAL PRIMARY KEY,
                user_email TEXT,
                topic TEXT,
                qtype TEXT,
                difficulty TEXT,
                score TEXT,
                percentage TEXT,
                questions JSONB,
                answers JSONB,
                attempted_at TIMESTAMP
            )
        """)
        print("🔁 Attempt being inserted:")
        print(json.dumps(attempt, indent=2))
        # ✅ Insert quiz data
        cursor.execute("""
            INSERT INTO quiz_attempts (
                user_email, topic, qtype, difficulty, score, percentage, questions, answers, attempted_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_email,
            attempt["topic"],
            attempt["type"],  # ✅ we use 'type' in Python, insert into qtype
            attempt["difficulty"],
            attempt["score"],
            attempt["percentage"],
            json.dumps(attempt["questions"]),
            json.dumps(attempt["answers"]),
            datetime.now()
        ))

        conn.commit()
        cursor.close()
        print("✅ Quiz attempt inserted successfully")
    except Exception as e:
        print("❌ DB INSERT FAILED:", e)

def get_attempts_for_user(conn, user_email):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT topic, qtype, difficulty, score, percentage, questions, answers, attempted_at
        FROM quiz_attempts
        WHERE user_email = %s
        ORDER BY attempted_at DESC
    """, (user_email,))

    rows = cursor.fetchall()
    attempts = []
    for row in rows:
        attempts.append({
            "topic": row[0],
            "type": row[1],  # map qtype to type
            "difficulty": row[2],
            "score": row[3],
            "percentage": row[4],
            "questions": row[5],  # ✅ no json.loads
            "answers": row[6],    # ✅ no json.loads
            "attempted_at": row[7]
        })
    
    cursor.close()
    return attempts
