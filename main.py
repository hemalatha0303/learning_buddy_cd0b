#main.py
import streamlit as st
import os
from signlog import show_auth_page

st.set_page_config(
    page_title="Learning Buddy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
from show_friends import show_friends_page
from show_landing_page import show_landing_page
from signlog import show_auth_page
from show_home import show_home, show_generate_quiz, show_flashcards, show_saved_content, show_settings
from show_home import show_profile

# Force watchdog to use polling instead of inotify (prevents inotify errors)
os.environ["STREAMLIT_WATCHDOG_USE_POLLING"] = "true"
os.environ["TOGETHER_API_KEY"] = st.secrets["together"]["TOGETHER_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["OPENAI_API_KEY"]

# Set default values
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = False
    st.session_state.page = 'landing'
    st.session_state.signed_in = False
    st.session_state.current_page = 'Home'

# Page routing logic
if st.session_state.page == 'landing':
    show_landing_page()

elif st.session_state.page == 'auth':
    show_auth_page()

elif st.session_state.page == 'signlog':
    st.session_state.page = 'auth'
    st.rerun()
elif st.session_state.page == 'forgot_password':
    show_auth_page()


elif st.session_state.page == 'home':
    if st.session_state.signed_in:
        match st.session_state.current_page.lower().replace(" ", "_"):
            case "home":
                show_home()
            case "generate_quiz":
                show_generate_quiz()
            case "flashcards":
                show_flashcards()
            case "saved_content":
                show_saved_content()
            case "settings":
                show_settings()
            case "profile":
                show_profile()
            case "friends":
                show_friends_page()
    else:
        st.session_state.page = 'signlog'
        show_auth_page()

# Handle profile dropdown actions from top-right corner
action = st.query_params.get("profile_action")

if action == "settings":
    st.session_state.current_page = "Settings"
    st.query_params.clear()
    st.rerun()

elif action == "logout":
    st.session_state.signed_in = False
    st.session_state.page = "landing"
    st.session_state.current_page = "Home"
    st.query_params.clear()
    st.rerun()
