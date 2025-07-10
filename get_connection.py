# get_connection.py
import psycopg2
from psycopg2 import OperationalError
import streamlit as st

def get_connection():
    try:
        db = st.secrets["database"]
        conn = psycopg2.connect(
            host=db["host"],
            port=db["port"],
            dbname=db["dbname"],
            user=db["user"],
            password=db["password"]
        )
        return conn
    except OperationalError as e:
        st.error(f"❌ Connection failed: {e}")
        return None
