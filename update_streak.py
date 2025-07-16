from datetime import date
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="signlog",
        user="postgres",
        password="postgre"
    )

def update_streak(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT last_quiz_date FROM users WHERE id = %s", (user_id,))
    last_date = cur.fetchone()[0]
    today = date.today()

    if last_date is not None and (today - last_date).days == 1:
        cur.execute("UPDATE users SET study_streak = study_streak + 1, last_quiz_date = %s WHERE id = %s", (today, user_id))
    elif last_date != today:
        cur.execute("UPDATE users SET study_streak = 1, last_quiz_date = %s WHERE id = %s", (today, user_id))

    conn.commit()
    cur.close()
    conn.close()
