import streamlit as st
import os
import uuid
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import firestore
from firebase_config import db

# --- Load secrets securely from Streamlit Cloud
SENDGRID_API_KEY = st.secrets.get("SENDGRID_API_KEY", "")
SENDER_EMAIL = st.secrets.get("SENDER_EMAIL", "")

# --- OTP Generator
def generate_otp():
    return str(uuid.uuid4())[:6].upper()

# --- Send OTP Email
def send_otp_email(to_email, otp):
    try:
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
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        st.error("❌ OTP sending failed. Check credentials or sender verification.")
        st.exception(e)
        return False

# --- Send Password Email
def send_password_email(to_email, password):
    try:
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=to_email,
            subject="🔐 Your Learning Buddy Password",
            html_content=f"""
                <p>Hello!</p>
                <p>Your password is: <strong>{password}</strong></p>
                <p>Keep it secure!</p>
            """
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        st.error("❌ Email sending failed.")
        st.exception(e)
        return False

# --- Auth Page
def show_auth_page():
    st.markdown('<div class="bg-animation"></div>', unsafe_allow_html=True)
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "page" not in st.session_state:
        st.session_state.page = "auth"

    if st.session_state.page == "auth":
        col1, col2, _ = st.columns([4, 4, 1])
        with col1:
            st.image("https://i.pinimg.com/736x/ce/05/0f/ce050f376fcfac459e5bad33c6dca557.jpg")

        with col2:
            st.markdown("## 👋 Welcome Back!")
            tab1, tab2 = st.tabs(["🔑 Sign In", "👤 Sign Up"])

            # Sign In
            with tab1:
                email = st.text_input("📧 Email")
                password = st.text_input("🔐 Password", type="password")

                if st.button("Sign In"):
                    if email and password:
                        users_ref = db.collection("users")
                        query = users_ref.where("email", "==", email).where("password", "==", password).stream()
                        user_doc = next(query, None)
                        if user_doc:
                            user_data = user_doc.to_dict()
                            if not user_data.get("is_verified"):
                                st.warning("⚠️ Email not verified.")
                            else:
                                st.session_state.update({
                                    "signed_in": True,
                                    "user_id": user_doc.id,
                                    "user_name": user_data.get("full_name"),
                                    "user_email": user_data.get("email"),
                                    "page": "home",
                                    "current_page": "Home"
                                })
                                today = datetime.now()
                                last_login = user_data.get("last_login_date")
                                streak = user_data.get("study_streak", 0)
                                new_streak = streak + 1 if last_login == (today - timedelta(days=1)) else 1

                                db.collection("users").document(user_doc.id).update({
                                    "study_streak": new_streak,
                                    "last_login_date": today
                                })
                                st.success("🎉 Signed in!")
                                st.rerun()
                        else:
                            st.error("❌ Invalid credentials.")

            # Sign Up
            with tab2:
                name = st.text_input("👤 Full Name")
                email = st.text_input("📧 Email")
                password = st.text_input("🔐 Password", type="password")
                confirm = st.text_input("🔐 Confirm Password", type="password")

                if st.button("Create Account"):
                    if name and email and password == confirm:
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
                                "created_at": datetime.now(),
                                "otp_code": otp,
                                "is_verified": False,
                                "study_streak": 0,
                                "last_login_date": None
                            })
                            if send_otp_email(email, otp):
                                st.session_state.verification_email = email
                                st.session_state.show_verification = True
                                st.success("🎉 Account created! Check your email for OTP.")
                            else:
                                st.error("❌ Failed to send OTP.")
                                st.code(traceback.format_exc())
                    else:
                        st.error("❗ Please fill all fields and match passwords.")

            # Verify OTP
            if st.session_state.get("show_verification"):
                st.markdown("### 🔐 Email Verification")
                otp_input = st.text_input("Enter OTP")
                if st.button("✅ Verify OTP"):
                    users_ref = db.collection("users").where("email", "==", st.session_state.verification_email)
                    user_doc = next(users_ref.stream(), None)
                    if user_doc and otp_input == user_doc.to_dict().get("otp_code"):
                        db.collection("users").document(user_doc.id).update({
                            "is_verified": True,
                            "otp_code": firestore.DELETE_FIELD
                        })
                        st.success("✅ Email verified!")
                        st.session_state.show_verification = False
                    else:
                        st.error("❌ Incorrect OTP.")

                if st.button("🔁 Resend OTP"):
                    new_otp = generate_otp()
                    users_ref = db.collection("users").where("email", "==", st.session_state.verification_email)
                    user_doc = next(users_ref.stream(), None)
                    if user_doc:
                        db.collection("users").document(user_doc.id).update({"otp_code": new_otp})
                        if send_otp_email(st.session_state.verification_email, new_otp):
                            st.success("✅ OTP resent.")
                        else:
                            st.error("❌ Failed to send OTP.")

    elif st.session_state.page == "forgot_password":
        st.markdown("## 🔐 Forgot Password")
        email_input = st.text_input("📧 Registered Email")
        if st.button("📨 Send Password"):
            query = db.collection("users").where("email", "==", email_input).stream()
            user_doc = next(query, None)
            if user_doc:
                password = user_doc.to_dict().get("password")
                if send_password_email(email_input, password):
                    st.success("✅ Password emailed.")
                else:
                    st.error("❌ Failed to send email.")
            else:
                st.error("🚫 Email not found.")

        if st.button("⬅️ Back to Sign In"):
            st.session_state.page = "auth"
            st.rerun()

    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #64748b; font-size: 0.9rem;">\ud83e\uddd0 Learning Buddy - Powered by Bright Minds | © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_auth_page()
