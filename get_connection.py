# get_connection.py
import psycopg2
from psycopg2 import OperationalError
import streamlit as st

def get_connection():
    try:
        db = st.secrets["database"]
        conn = psycopg2.connect(
            host="aws-0-ap-south-1.pooler.supabase.com",
            port="6543",
            database="postgres",
            user="postgres",
            password="Hema!@#7254"
            sslmode="require"  # 🔒 this line is crucial
        )
        return conn
    except OperationalError as e:
        st.error(f"❌ Connection failed: {e}")
        return None
