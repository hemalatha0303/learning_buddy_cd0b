import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import tempfile
import json
import os

@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred_json = st.secrets["firebase"]["FIREBASE_CREDENTIALS_JSON"]
        data = json.loads(cred_json)

        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as f:
            json.dump(data, f)
            tmp_path = f.name

        cred = credentials.Certificate(tmp_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()
