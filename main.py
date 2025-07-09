#main.py
import streamlit as st

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
        if st.session_state.current_page == 'Home':
            show_home()
        elif st.session_state.current_page == 'Generate Quiz':
            show_generate_quiz()
        elif st.session_state.current_page == 'Flashcards':
            show_flashcards()
        elif st.session_state.current_page == 'Saved Content':
            show_saved_content()
        elif st.session_state.current_page == 'Settings':
            show_settings()
        elif st.session_state.current_page == "profile":
            show_profile()
        elif st.session_state.current_page == "Friends":
            show_friends_page()
        elif st.session_state.page == "home":
            show_home()
        #elif st.session_state.page == 'forgot_password':
            #show_auth_page()  # because forgot_password is handled inside signlog.py


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
