
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
import os
import uuid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
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


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="signlog",
        user="postgres",
        password="postgre"
    )
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
                    if st.session_state.signin_email and st.session_state.signin_password:
                        try:
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("""
                                SELECT * FROM users WHERE email = %s AND password = %s
                            """, (
                                st.session_state.signin_email,
                                st.session_state.signin_password
                            ))
                            user = cur.fetchone()

                            if user:
                                user_id = user[0]
                                full_name = user[1]
                                email = user[2]
                                is_verified = user[9]
                                if not is_verified:
                                    st.warning("⚠️ Your email is not verified. Please check your OTP or sign up again.")
                                else:
                                    st.session_state.signed_in = True
                                    st.session_state.user_id = user[0]
                                    st.session_state.user_name = user[1]
                                    st.session_state.user_email = user[2]
                                    st.session_state.page = 'home'
                                    st.session_state.current_page = 'Home'
                                    st.success("🎉 Successfully signed in! Welcome back.")
                                    

                                    try:
                                        today = datetime.now().date()
                                        cur.execute("SELECT study_streak, last_login_date FROM users WHERE id = %s", (st.session_state.user_id,))
                                        result = cur.fetchone()

                                        if result:
                                            current_streak, last_login = result
                                            if last_login == today:
                                                new_streak = current_streak
                                            elif last_login == today - timedelta(days=1):
                                                new_streak = current_streak + 1
                                            else:
                                                new_streak = 1
                                        else:
                                            new_streak = 1

                                        cur.execute("""
                                            UPDATE users 
                                            SET study_streak = %s,
                                                last_login_date = %s
                                            WHERE id = %s
                                        """, (new_streak, today, st.session_state.user_id))
                                        conn.commit()

                                    except Exception as e:
                                        st.error(f"⚠️ Failed to update login streak: {e}")

                                    finally:
                                        cur.close()
                                        conn.close()

                                    st.rerun()
                            else:
                                    st.error("❌ Invalid email or password")
    
                        except Exception as e:
                            st.error(f"Database error: {e}")

            with tab2:
                st.text_input("👤 Full Name", placeholder="Enter your full name", key="signup_name")
                st.text_input("📧 Email Address", placeholder="Enter your email", key="signup_email")
                st.text_input("🔐 Password", placeholder="Create a strong password", type="password", key="signup_password")
                st.text_input("🔐 Confirm Password", placeholder="Re-enter your password", type="password", key="confirm_password")

                if st.button("Create Account", key="signup_btn"):
                    if (st.session_state.signup_name and st.session_state.signup_email and 
                        st.session_state.signup_password and st.session_state.confirm_password):
                        
                        if st.session_state.signup_password == st.session_state.confirm_password:
                            try:
                                otp = generate_otp()
                                conn = get_connection()
                                cur = conn.cursor()

                                cur.execute("""
                                    INSERT INTO users (full_name, email, password, created_at, otp_code, is_verified)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    st.session_state.signup_name,
                                    st.session_state.signup_email,
                                    st.session_state.signup_password,
                                    datetime.now(),
                                    otp,
                                    False
                                ))
                                conn.commit()
                                cur.close()
                                conn.close()

                                email_sent = send_otp_email(st.session_state.signup_email, otp)
                                if email_sent:
                                    st.success("🎉 Account created! OTP sent to your email.")
                                    st.session_state.verification_email = st.session_state.signup_email
                                    st.session_state.show_verification = True
                                else:
                                    st.error("❌ Failed to send OTP. Please try again.")

                            except psycopg2.errors.UniqueViolation:
                                st.error("⚠️ This email is already registered.")
                            except Exception as e:
                                st.error(f"Database error: {e}")
                        else:
                            st.error("❌ Passwords don't match.")
                    else:
                        st.error("❗ All fields are required.")

                # 🔐 OTP Verification UI
                if st.session_state.get("show_verification", False):
                    st.markdown("### 🔐 Email Verification")
                    otp_input = st.text_input("Enter the OTP sent to your email:")

                    if st.button("✅ Verify OTP"):
                        try:
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("SELECT otp_code FROM users WHERE email = %s", (st.session_state.verification_email,))
                            row = cur.fetchone()

                            if row and otp_input == row[0]:
                                cur.execute("""
                                    UPDATE users SET is_verified = TRUE, otp_code = NULL WHERE email = %s
                                """, (st.session_state.verification_email,))
                                conn.commit()
                                st.success("✅ Email verified! You can now sign in.")
                                st.session_state.show_verification = False
                            else:
                                st.error("❌ Incorrect OTP.")

                        except Exception as e:
                            st.error(f"Database error: {e}")
                        finally:
                            cur.close()
                            conn.close()

                    if st.button("🔁 Resend OTP"):
                        new_otp = generate_otp()
                        try:
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("""
                                UPDATE users SET otp_code = %s WHERE email = %s
                            """, (new_otp, st.session_state.verification_email))
                            conn.commit()
                            cur.close()
                            conn.close()

                            email_sent = send_otp_email(st.session_state.verification_email, new_otp)
                            if email_sent:
                                st.success("✅ OTP resent to your email.")
                            else:
                                st.error("❌ Failed to resend OTP.")

                        except Exception as e:
                            st.error(f"Database error: {e}")
            
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
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("SELECT password FROM users WHERE email = %s", (email_input,))
                    result = cur.fetchone()
                    cur.close()
                    conn.close()

                    if result:
                        success = send_password_email(email_input, result[0])
                        if success:
                            st.success("✅ Password has been emailed to your inbox.")
                        else:
                            st.error("❌ Failed to send email. Please try again.")
                    else:
                        st.error("🚫 No user found with that email.")
                except Exception as e:
                    st.error(f"⚠️ Database Error: {e}")

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
