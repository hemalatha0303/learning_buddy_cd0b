# signlog.py
import streamlit as st
import uuid
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import firestore
from firebase_config import db  # Firestore client

# 🔐 Secrets
SENDGRID_API_KEY = st.secrets["sendgrid"]["SENDGRID_API_KEY"]
SENDER_EMAIL = st.secrets["sendgrid"]["SENDER_EMAIL"]

# 🔑 Utility

def generate_otp():
    return str(uuid.uuid4())[:6].upper()

def send_otp_email(email, otp):
    try:
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=email,
            subject="Your OTP Code",
            plain_text_content=f"Your OTP for Learning Buddy is: {otp}"
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        st.error("SendGrid OTP Email Failed")
        st.write(e)
        return False

def send_password_email(to_email, password):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject="🔐 Your Learning Buddy Password",
        html_content=f"""
            <p>Your password is: <strong>{password}</strong></p>
            <p>Login and update your credentials securely.</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        return sg.send(message).status_code == 202
    except Exception as e:
        st.error("SendGrid Password Email Failed")
        st.write(e)
        return False

# 🧠 Main Auth Page

def show_auth_page():
    from show_home import show_home

    if "page" not in st.session_state:
        st.session_state.page = "auth"

    if st.session_state.page == "auth":
        show_signin_signup()
    elif st.session_state.page == "forgot_password":
        show_forgot_password()

    st.markdown("---")
    st.markdown('<div style="text-align:center;color:#64748b;font-size:0.9rem;">\n🧠 Learning Buddy - Powered by Bright Minds | © 2025</div>', unsafe_allow_html=True)

# 🧾 Sign In / Sign Up UI

def show_signin_signup():
    st.title("🔐 Welcome Back to Learning Buddy")
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="signin_email")
        password = st.text_input("Password", type="password", key="signin_password")

        if st.button("Sign In"):
            user_doc = db.collection("users").where("email", "==", email).where("password", "==", password).stream()
            user_doc = next(user_doc, None)
            if user_doc:
                user_data = user_doc.to_dict()
                if user_data.get("is_verified"):
                    st.session_state.signed_in = True
                    st.session_state.user_email = user_data["email"]
                    st.session_state.page = "home"
                    db.collection("users").document(user_doc.id).update({
                        "last_login_date": datetime.now(),
                        "study_streak": user_data.get("study_streak", 0) + 1
                    })
                    st.success("✅ Signed in successfully!")
                    st.rerun()
                else:
                    st.warning("⚠️ Email not verified.")
            else:
                st.error("❌ Invalid credentials.")

        if st.button("Forgot Password"):
            st.session_state.page = "forgot_password"
            st.rerun()

    with tab2:
        name = st.text_input("Full Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Create Account"):
            if password != confirm:
                st.error("Passwords do not match.")
                return

            otp = generate_otp()
            if send_otp_email(email, otp):
                db.collection("users").add({
                    "full_name": name,
                    "email": email,
                    "password": password,
                    "is_verified": False,
                    "otp_code": otp,
                    "study_streak": 0,
                    "last_login_date": None,
                    "created_at": datetime.now()
                })
                st.success("✅ OTP sent. Please verify email.")
                st.session_state.verification_email = email
                st.session_state.page = "verify_otp"
                st.rerun()
            else:
                st.error("Failed to send OTP.")

# 🔓 Forgot Password UI

def show_forgot_password():
    st.header("🔑 Forgot Password")
    email = st.text_input("Registered Email", key="forgot_email")

    if st.button("📨 Email Password"):
        user_doc = db.collection("users").where("email", "==", email).stream()
        user_doc = next(user_doc, None)
        if user_doc:
            password = user_doc.to_dict().get("password")
            if send_password_email(email, password):
                st.success("✅ Password sent to email.")
            else:
                st.error("❌ Failed to send email.")
        else:
            st.error("No user with that email.")

    if st.button("⬅ Back"):
        st.session_state.page = "auth"
        st.rerun()

# 🔁 Entrypoint

if __name__ == "__main__":
    show_auth_page()
