import firebase_admin
from firebase_admin import credentials, firestore
import json
import streamlit as st

@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        cred = credentials.Certificate(json.loads(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_db()
