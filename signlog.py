
# signlog.py
import streamlit as st
import psycopg2
import psycopg2.errors
from datetime import datetime, timedelta
from show_home import show_home
import smtplib
from email.message import EmailMessage
import random
import string
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_config import db  # Ensure Firestore is initialized
import os
import uuid
from firebase_admin import firestore

firestore.DELETE_FIELD  # <-- works only when needed

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from firebase_config import db  # Import Firestore client
from datetime import datetime
import json

# signlog.py
SENDGRID_API_KEY = st.secrets["sendgrid"]["SENDGRID_API_KEY"]
SENDER_EMAIL = st.secrets["sendgrid"]["SENDER_EMAIL"]
import os
import streamlit as st

os.environ["TOGETHER_API_KEY"] = st.secrets["together"]["TOGETHER_API_KEY"]

def generate_otp():
    return str(uuid.uuid4())[:6].upper()  # 6-char OTP

def send_otp_email(to_email, otp):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject="Your OTP for AI Quiz Generator",
        html_content=f"""
        <p>Hello!</p>
        <p>Your One-Time Password (OTP) is: <strong>{otp}</strong></p>
        <p>Please use this to verify your email.</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"SendGrid response: {response.status_code}, body: {response.body}, headers: {response.headers}")
        return response.status_code == 202
    except Exception as e:
        print(f"SendGrid Error: {e}")
        return False

def send_password_email(to_email, password):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject="🔐 Your Learning Buddy Password",
        html_content=f"""
            <p>Hello!</p>
            <p>Your password is: <strong>{password}</strong></p>
            <p>Please use this to log in and keep it secure.</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("✅ SendGrid:", response.status_code)
        return response.status_code == 202
    except Exception as e:
        print("❌ SendGrid Error:", e)
        return False


def show_auth_page():
    st.markdown('<div class="bg-animation"></div>', unsafe_allow_html=True)
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        # 🔁 When Forgot Password → Back to Sign In:
        

    if "page" not in st.session_state:
        st.session_state.page = "auth"

    for key in ["signin_email", "signin_password"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    if st.session_state.page == "auth": 
        if st.button("⬅️ Back to landing"):
                        st.session_state.page = "landing"
                        st.rerun()    
        col1, col2,col3 = st.columns([4, 4, 1])
        with col1:
                        
            st.markdown("""
            <style>
                .info-box {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 30px;
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: white;
                    border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    animation: fadeIn 2s ease-in-out;
                }

                .info-content {
                    max-width: 800px;
                    text-align: center;
                    font-size: 1.2rem;
                    line-height: 1.8;
                }

                .info-title {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    color: #ffffff;
                    text-shadow: 1px 1px 8px black;
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>

            <div class="info-box">
                <div class="info-content">
                    <div class="info-title">🧠 Welcome to Learning Buddy</div>
                    <img src="https://i.pinimg.com/736x/ce/05/0f/ce050f376fcfac459e5bad33c6dca557.jpg">
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="right-panel fade-in">
                <div class="welcome-header">
                    <h1 class="hero-title" style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>Welcome back!</h1>
                    <p class="hero-subtitle">Sign in to access your AI-generated quizzes and start learning smarter.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔑 Sign In", "👤 Sign Up"])

            with tab1:
                st.text_input("📧 Email Address", placeholder="Enter your email", key="signin_email")
                st.text_input("🔐 Password", placeholder="Enter your password", type="password", key="signin_password")
            
                if st.button("❓ Forgot Password"):
                    st.session_state.page = "forgot_password"
                    st.rerun()
            
                if st.button("Sign In", key="signin_btn"):
                    email = st.session_state.signin_email.strip().lower()
                    password = st.session_state.signin_password.strip()
            
                    if email and password:
                        with st.spinner("Signing you in..."):
                            try:
                                users_ref = db.collection("users").where("email", "==", email).limit(1).stream()
                                user_doc = next(users_ref, None)
            
                                if user_doc:
                                    user_data = user_doc.to_dict()
            
                                    if password != user_data.get("password"):
                                        st.error("❌ Invalid email or password")
                                    elif not user_data.get("is_verified", False):
                                        st.warning("⚠️ Your email is not verified.")
                                    else:
                                        # ✅ Login success
                                        st.session_state.signed_in = True
                                        st.session_state.user_id = user_doc.id
                                        st.session_state.user_name = user_data.get("full_name")
                                        st.session_state.user_email = user_data.get("email")
                                        st.session_state.page = 'home'
                                        st.session_state.current_page = 'Home'
                                        st.success("🎉 Successfully signed in! Welcome back.")
            
                                        # 🔄 Update login streak
                                        today = datetime.now().date()
                                        last_login = user_data.get("last_login_date")
                                        streak = user_data.get("study_streak", 0)
            
                                        if last_login == today:
                                            new_streak = streak
                                        elif last_login == (today - timedelta(days=1)):
                                            new_streak = streak + 1
                                        else:
                                            new_streak = 1
            
                                        db.collection("users").document(user_doc.id).update({
                                            "study_streak": new_streak,
                                            "last_login_date": today
                                        })
            
                                        st.rerun()
                                else:
                                    st.error("❌ Invalid email or password")
                            except Exception as e:
                                st.error(f"🔥 Firebase error: {str(e)}")
            
            
            # -------------------- 👤 SIGN UP TAB --------------------
            with tab2:
                st.text_input("👤 Full Name", placeholder="Enter your full name", key="signup_name")
                st.text_input("📧 Email Address", placeholder="Enter your email", key="signup_email")
                st.text_input("🔐 Password", placeholder="Create a strong password", type="password", key="signup_password")
                st.text_input("🔐 Confirm Password", placeholder="Re-enter your password", type="password", key="confirm_password")
            
                if st.button("Create Account", key="signup_btn"):
                    name = st.session_state.signup_name.strip()
                    email = st.session_state.signup_email.strip().lower()
                    password = st.session_state.signup_password.strip()
                    confirm = st.session_state.confirm_password.strip()
            
                    if name and email and password and confirm:
                        if password != confirm:
                            st.error("❌ Passwords don't match.")
                        else:
                            with st.spinner("Creating your account..."):
                                try:
                                    users_ref = db.collection("users")
                                    existing_user = next(users_ref.where("email", "==", email).limit(1).stream(), None)
            
                                    if existing_user:
                                        st.error("⚠️ Email already registered.")
                                    else:
                                        otp = generate_otp()
                                        db.collection("users").add({
                                            "full_name": name,
                                            "email": email,
                                            "password": password,
                                            "created_at": firestore.SERVER_TIMESTAMP,
                                            "otp_code": otp,
                                            "is_verified": False,
                                            "study_streak": 0,
                                            "last_login_date": None
                                        })
            
                                        if send_otp_email(email, otp):
                                            st.success("🎉 Account created! OTP sent to your email.")
                                            st.session_state.verification_email = email
                                            st.session_state.show_verification = True
                                        else:
                                            st.error("❌ Failed to send OTP.")
                                except Exception as e:
                                    st.error(f"🔥 Firebase error: {str(e)}")
                    else:
                        st.error("❗ All fields are required.")
            
                # -------------------- 🔐 OTP VERIFICATION --------------------
                if st.session_state.get("show_verification", False):
                    st.markdown("### 🔐 Email Verification")
                    otp_input = st.text_input("Enter the OTP sent to your email:")
            
                    if st.button("✅ Verify OTP"):
                        with st.spinner("Verifying..."):
                            try:
                                users_ref = db.collection("users").where("email", "==", st.session_state.verification_email)
                                user_doc = next(users_ref.stream(), None)
            
                                if user_doc and otp_input == user_doc.to_dict().get("otp_code"):
                                    db.collection("users").document(user_doc.id).update({
                                        "is_verified": True,
                                        "otp_code": firestore.DELETE_FIELD
                                    })
                                    st.success("✅ Email verified! You can now sign in.")
                                    st.session_state.show_verification = False
                                else:
                                    st.error("❌ Incorrect OTP.")
                            except Exception as e:
                                st.error(f"🔥 Firebase error: {str(e)}")
            
                    if st.button("🔁 Resend OTP"):
                        try:
                            new_otp = generate_otp()
                            users_ref = db.collection("users").where("email", "==", st.session_state.verification_email)
                            user_doc = next(users_ref.stream(), None)
            
                            if user_doc:
                                db.collection("users").document(user_doc.id).update({"otp_code": new_otp})
                                if send_otp_email(st.session_state.verification_email, new_otp):
                                    st.success("✅ OTP resent.")
                                else:
                                    st.error("❌ Failed to send OTP.")
                        except Exception as e:
                            st.error(f"🔥 Firebase error: {str(e)}")

            
    elif st.session_state.page == "forgot_password":

        col1,col2,col3 = st.columns([4,4,2])
        with col1:
            st.markdown("""
            <style>
                .info-box {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 30px;
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                    color: white;
                    border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    animation: fadeIn 2s ease-in-out;
                }

                .info-content {
                    max-width: 800px;
                    text-align: center;
                    font-size: 1.2rem;
                    line-height: 1.8;
                }

                .info-title {
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    color: #ffffff;
                    text-shadow: 1px 1px 8px black;
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(30px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>

            <div class="info-box">
                <div class="info-content">
                    <div class="info-title">🧠 Welcome to Learning Buddy</div>
                    <img src="https://i.pinimg.com/736x/ce/05/0f/ce050f376fcfac459e5bad33c6dca557.jpg">
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("## 🔐 Forgot Password", unsafe_allow_html=True)
            st.markdown("Enter your registered email address to receive your password via email.", unsafe_allow_html=True)
                        
                        
            email_input = st.text_input("📧 Registered Email", placeholder="you@example.com", key="forgot_email")

            if st.button("📨 Send Password to Email"):
                try:
                    query = db.collection("users").where("email", "==", email_input).stream()
                    user_doc = next(query, None)

                    if user_doc:
                        password = user_doc.to_dict().get("password")
                        success = send_password_email(email_input, password)
                        if success:
                            st.success("✅ Password has been emailed to your inbox.")
                        else:
                            st.error("❌ Failed to send email. Please try again.")
                    else:
                        st.error("🚫 No user found with that email.")
                except Exception as e:
                    st.error(f"⚠️ Firebase Error: {e}")

            # 🔁 When Forgot Password → Back to Sign In:
            if st.button("⬅️ Back to Sign In"):
                st.session_state.page = "signlog"
                st.rerun()



            

    # ------------------------ Footer ------------------------
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds | © 2025</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show_auth_page()
