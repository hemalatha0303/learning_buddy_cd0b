import firebase_admin
from firebase_admin import credentials, firestore
import json
import streamlit as st

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        json_str = st.secrets["firebase"]["FIREBASE_CREDENTIALS_JSON"]
        cred_dict = json.loads(json_str)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()
