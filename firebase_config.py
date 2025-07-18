import firebase_admin
from firebase_admin import credentials, firestore
import tempfile
import streamlit as st

@st.cache_resource
def init_firebase():
    firebase_creds_json = st.secrets["firebase"]["FIREBASE_CREDENTIALS_JSON"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmp:
        tmp.write(firebase_creds_json)
        tmp_path = tmp.name

    cred = credentials.Certificate(tmp_path)

    # Avoid re-initializing if already done
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()
