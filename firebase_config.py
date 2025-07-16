import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

if not cred_json:
    raise ValueError("🔥 FIREBASE_CREDENTIALS_JSON is not set in Streamlit secrets or environment variables.")

cred = credentials.Certificate(json.loads(cred_json))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
