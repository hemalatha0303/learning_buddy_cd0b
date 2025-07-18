import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_credentials.json")  # Place this file securely
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()
