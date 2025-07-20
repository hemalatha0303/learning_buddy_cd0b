import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred)

db = firestore.client()

st.set_page_config(page_title="Learning Buddy", page_icon="🧠", layout="centered")
st.title("\U0001F9E0 Welcome to Learning Buddy")

st.markdown("Sign in to access your AI-generated quizzes and start learning smarter.")

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP email
def send_email(recipient_email, otp):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"
    subject = "Your Learning Buddy OTP Code"
    body = f"Your OTP code is: {otp}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()

# Initialize session states
if "signed_in" not in st.session_state:
    st.session_state.signed_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "verification_email" not in st.session_state:
    st.session_state.verification_email = ""
if "show_verification" not in st.session_state:
    st.session_state.show_verification = False

# Sign In / Sign Up Tabs
tab1, tab2 = st.tabs(["🔑 Sign In", "👤 Sign Up"])

with tab1:
    st.subheader("Welcome back!")
    email = st.text_input("📧 Email", key="signin_email")
    password = st.text_input("🔐 Password", type="password", key="signin_password")

    if st.button("Sign In"):
        users_ref = db.collection("users").where("email", "==", email).where("password", "==", password)
        user = next(users_ref.stream(), None)
        if user:
            user_dict = user.to_dict()
            if user_dict.get("is_verified", False):
                st.session_state.signed_in = True
                st.session_state.current_page = "Dashboard"
                st.success("Successfully signed in!")
            else:
                st.warning("Please verify your email before signing in.")
        else:
            st.error("Invalid email or password")

with tab2:
    st.subheader("Create an Account")
    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email Address")
    password = st.text_input("🔐 Password", type="password")
    confirm_password = st.text_input("🔐 Confirm Password", type="password")

    if st.button("Create Account"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            # Check if email already exists
            users_ref = db.collection("users").where("email", "==", email).get()
            pending_ref = db.collection("pending_users").document(email).get()
            if users_ref or pending_ref.exists:
                st.error("⚠️ Email already registered.")
            else:
                otp = generate_otp()
                db.collection("pending_users").document(email).set({
                    "full_name": name,
                    "email": email,
                    "password": password,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "otp_code": otp
                })
                send_email(email, otp)
                st.session_state.verification_email = email
                st.session_state.show_verification = True
                st.success("OTP sent to your email. Please verify.")

# OTP Verification
if st.session_state.show_verification:
    st.subheader("Verify Email")
    otp_input = st.text_input("Enter the OTP sent to your email")
    if st.button("Verify"):
        pending_ref = db.collection("pending_users").document(st.session_state.verification_email)
        pending_doc = pending_ref.get()

        if pending_doc.exists and otp_input == pending_doc.to_dict().get("otp_code"):
            user_data = pending_doc.to_dict()
            db.collection("users").add({
                "full_name": user_data["full_name"],
                "email": user_data["email"],
                "password": user_data["password"],
                "created_at": firestore.SERVER_TIMESTAMP,
                "is_verified": True,
                "study_streak": 0,
                "last_login_date": None
            })
            pending_ref.delete()
            st.session_state.show_verification = False
            st.success("✅ Email verified! You can now sign in.")
        else:
            st.error("❌ Incorrect OTP")

    if st.button("Resend OTP"):
        pending_ref = db.collection("pending_users").document(st.session_state.verification_email)
        pending_doc = pending_ref.get()
        if pending_doc.exists:
            new_otp = generate_otp()
            pending_ref.update({"otp_code": new_otp})
            send_email(st.session_state.verification_email, new_otp)
            st.success("A new OTP has been sent to your email.")
