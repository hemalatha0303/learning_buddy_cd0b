import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import tempfile
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def init_firebase():
    cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmp:
        tmp.write(cred_json)
        tmp_path = tmp.name

    cred = credentials.Certificate(tmp_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()
