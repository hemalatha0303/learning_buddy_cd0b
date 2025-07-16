# friends_list.py
from firebase_config import db

def get_friends_list(user_id):
    """
    Fetches a list of friends for the given user_id from Firestore.
    Returns:
        List of tuples: (full_name, study_streak, email)
    """
    friends = []
    try:
        # Get all friend_ids from the 'friends' collection
        friend_docs = db.collection("friends").where("user_id", "==", user_id).stream()
        
        for friend_doc in friend_docs:
            friend_data = friend_doc.to_dict()
            friend_id = friend_data.get("friend_id")

            if not friend_id:
                continue

            # Fetch user details from the 'users' collection
            user_doc = db.collection("users").document(friend_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                friends.append((
                    user_data.get("full_name", "Unknown"),
                    user_data.get("study_streak", 0),
                    user_data.get("email", "N/A")
                ))
    except Exception as e:
        print(f"❌ Firestore Error: {e}")
    
    return friends
