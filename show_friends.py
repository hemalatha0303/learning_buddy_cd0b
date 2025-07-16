# show_friends.py
from firebase_config import db
import streamlit as st

def show_friends_page():
    # Custom CSS for styling
    st.markdown("""
    <style>
        /* Main theme colors */
        .stApp {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: #0f172a;
        }
        
        /* Metric cards styling */
        .metric-card {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        }
        
        .metric-card-green {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        }
        
        .metric-card-purple {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        }
        
        .metric-card-orange {
            background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        }
        
        .metric-number {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 0.3rem;
        }
        
        .metric-sublabel {
            font-size: 0.9rem;
            opacity: 0.7;
        }
        
        /* Welcome message */
        .welcome-header {
            color: #f8fafc;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        .welcome-subtext {
            color: #cbd5e1;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Section headers */
        .section-header {
            color: #f8fafc;
            font-size: 1.8rem;
            font-weight: bold;
            margin: 2rem 0 1rem 0;
        }
        
        /* Generate button styling */
        .generate-btn {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            border: none;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        /* Make radio option labels white */
    div[role="radiogroup"] > label {
        color: white !important;
    }

    /* Make the text inside the radio label white */
    div[role="radiogroup"] > label > div:first-child {
        color: white !important;
    }

    /* For newer versions of Streamlit that render differently */
    label[data-baseweb="radio"] {
        color: white !important;
    }

                

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
                
        /* Make st.radio options white */
        div[role="radiogroup"] label {
        color: white !important;
    }

                

        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Sidebar navigation styling */
        .nav-item {
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #cbd5e1;
        }
        
        .nav-item:hover {
            background: #334155;
            color: #f8fafc;
        }
        
        .nav-item.active {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
        }
        label[data-testid="stRadio"] > div > label {
            color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'

    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h2 style='color: #f8fafc; margin-bottom: 2rem;'>🧠 AI Quiz Generator</h2>", unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content', '👤 profile', '⚙️ Settings']
        
        for page in pages:
            if st.button(page, key=page, use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]
    col1, col2 = st.columns([4,1])
    
        
    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'
    
    st.markdown('<div class="welcome-header" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">👥 All Users & Their Study Streaks</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtext" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">🔥 Ordered by highest streak</div>', unsafe_allow_html=True)
    
    # Fetch all users with non-null streaks
    try:
        users_ref = db.collection("users").where("study_streak", "!=", None)
        users = sorted(users_ref.stream(), key=lambda doc: doc.to_dict().get("study_streak", 0), reverse=True)
    except Exception as e:
        st.error(f"❌ Firebase error: {e}")
        return

    if not users:
        st.info("No users with streaks found.")
        return

    for i, user_doc in enumerate(users, start=1):
        user = user_doc.to_dict()
        name = user.get("full_name", "Unnamed")
        streak = user.get("study_streak", 0)
        st.markdown(f"""
        <div style="padding: 1rem;color:white; background: black; border-left: 5px solid #7e57c2; border-radius: 8px; margin-bottom: 1rem;">
            <strong>{i}. {name}</strong> <br><br>
            🔥 Streak: <strong>{streak} Days</strong>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds cd0b | © 2025'
        '</div>', 
        unsafe_allow_html=True
    ) 

