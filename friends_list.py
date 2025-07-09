# friends_list.py
from get_connection import get_connection

def get_friends_list(user_id):
    """
    Fetches a list of friends for the given user_id.

    Returns:
        List of tuples (full_name, study_streak, email)
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.full_name, u.study_streak, u.email
            FROM friends f
            JOIN users u ON f.friend_id = u.id
            WHERE f.user_id = %s
        """, (user_id,))
        friends = cur.fetchall()
    except Exception as e:
        print(f"❌ Error fetching friends: {e}")
        friends = []
    finally:
        if cur: cur.close()
        if conn: conn.close()
    
    return friends
