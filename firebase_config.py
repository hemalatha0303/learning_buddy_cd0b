import json
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

cred_json = st.secrets["firebase"]["FIREBASE_CREDENTIALS_JSON"]
cred = credentials.Certificate(json.loads(cred_json))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
