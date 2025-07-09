
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from quiz_generator import generate_quiz
from flash_cards_gen import generate_flashcards
import streamlit as st
import json
from saved_db import save_quiz_attempt, get_attempts_for_user
# --- Handle Profile Actions via Query Params ---
from urllib.parse import unquote
from get_connection import get_connection
import streamlit.components.v1 as components
import html
from update_streak import update_streak
from fpdf import FPDF
import tempfile
import streamlit.components.v1 as components
import html
from fpdf import FPDF
import os
import uuid
from show_friends import show_friends_page
from friends_list import get_friends_list
# Main content area

def show_home():
    # --- CSS Styling ---
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        }
        .metric-card, .metric-card-green, .metric-card-purple, .metric-card-orange {
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        }
        .metric-card-green {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        }
        .metric-card-orange {
            background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
            cursor: pointer;
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
        .section-header {
            color: #f8fafc;
            font-size: 1.8rem;
            font-weight: bold;
            margin: 2rem 0 1rem 0;
        }
        .topbar {
            display: flex;
            justify-content: flex-end;
            padding: 0.5rem 1rem 0 0;
        }
        .profile-btn {{
            background-color: #3b82f6;
            color: white;
            padding: 0.6rem 1.2rem;
            border: none;
            border-radius: 20px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
        }}
        .profile-menu {{
            display: none;
            position: absolute;
            right: 0;
            background-color: #1e293b;
            border-radius: 8px;
            margin-top: 0.5rem;
            min-width: 150px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            z-index: 100;
            overflow: hidden;
        }}
        .profile-menu a {{
            color: white;
            padding: 12px 16px;
            display: block;
            text-decoration: none;
        }}
        .profile-menu a:hover {{
            background-color: #334155;
        }}
        .topbar {{
            position: relative;
            display: flex;
            justify-content: flex-end;
            padding: 1rem;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff; margin-bottom: 2rem; '>🧠 Learning Buddy</h2>", unsafe_allow_html=True)
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content', '👤 profile', '⚙️ Settings']
        for i, page in enumerate(pages):
            if st.button(page, key=f"sidebar_nav_{i}", use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]
    col1, col2 = st.columns([4,1])
    
    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'

    query_page = st.query_params.get("current_page")
    if query_page:
        st.session_state.current_page = query_page
            # Add custom CSS styling
    
    # Inject Custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Initialize session states
    for key in ['show_signup', 'show_signin']:
        if key not in st.session_state:
            st.session_state[key] = False

    # Animated Background
    st.markdown('<div class="bg-animation"></div>', unsafe_allow_html=True)

    
        
    # Ensure these session variables are already set in your app
    st.session_state.setdefault("user_name", "User")
    st.session_state.setdefault("study_streak", 0)

    # Display welcome message
    st.markdown(f"""
    <div style="
        background: linear-gradient(#F97001, #1e40af 0%, #A4A4A4 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
    ">
        <h2 style="margin-bottom: 0.5rem;">🧠 Welcome back, <span style="color: #e0f2fe;">{st.session_state.user_name}</span>!</h2>
        <p style="font-size: 1.2rem;">You're on a <strong>{st.session_state.study_streak}-day streak</strong>. Let’s keep it going! 🔥</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<div class="section-header fade-in"  style='text-align: center;'>
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>Powerful Features</h2>
            <p class="section-subtitle" style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>Discover the comprehensive suite of tools designed to revolutionize your educational experience.</p>
        </div>""", unsafe_allow_html=True)
                
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card zoom-in">
            <h3>📝 Smart Quizzes</h3>
            <p>Generate personalized quizzes with AI that adapts to your learning level.</p>
            <strong>🎯 Adaptive Learning</strong>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card zoom-in">
            <h3>🗂️ Flashcards</h3>
            <p>Create interactive study flashcards that make memorization effective and fun.</p>
            <strong>🧠 Memory Boost</strong>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div  class="feature-card zoom-in">
            <h3>📊 Progress Tracking</h3>
            <p>Monitor your learning with insights, analytics, and achievements.</p>
            <strong>📈 Stay Motivated</strong>
        </div>
        """, unsafe_allow_html=True)


    # ---------- Features ----------
    st.markdown("""
    <div class="section">
        <h2 style='text-align: center; color: white; margin: 2rem 0; text-shadow: 0 0 10px #C66727;'>🚀 Why Students Love Learning Buddy</h2>
        
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box feature-card zoom-in" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-size:20px; color: white;">
            <h3>✨ Key Features</h3>
            <ul style="text-align: left; font-size: 1rem; line-height: 2;">
                <li>🎯 AI-generated quizzes and flashcards</li>
                <li>📈 Analytics and progress tracking</li>
                <li>🔥 Learning streaks & achievements</li>
                <li>👥 Connect with learners</li>
                <li>💾 Save your content</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box feature-card zoom-in" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);  font-size:20px;color: white;">
            <h3>🎁 Credit System</h3>
            <ul style="text-align: left; font-size: 1rem; line-height: 2;">
                <li>🆓 <strong>10 FREE credits</strong> at sign up</li>
                <li>📝 <strong>2 credits</strong> per quiz</li>
                <li>🗂️ <strong>1 credit</strong> per flashcard</li>
                <li>💾 Save your content</li>
                <li>💳 Buy more anytime: <strong>20 credits = 200/-</li>
            </ul>
            <p></p>
            <p></p>
            <p></p>
            <p></strong></p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box feature-card zoom-in" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); font-size:20px; color: white;">
            <h3>🎓 Perfect For</h3>
            <ul style="text-align: left; padding:top-padding;">
                <li>📚 High School Students</li>
                <li>🎓 College Students</li>
                <li>👨‍🏫 Test Preparation</li>
                <li>🧠 Lifelong Learners</li>
            </ul>
            <br>
        </div>
        """, unsafe_allow_html=True)
        
        # ---------- Horizontal Footer Stats ----------
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #94a3b8;'>Trusted by Global Educators</h4>", unsafe_allow_html=True)

    col0, col1, col2, col3, col4 = st.columns([1, 2, 2, 2, 2])

    with col1:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>25K+</h2>
            <p style='color:#cbd5e1;'>Active Educators</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>5M+</h2>
            <p style='color:#cbd5e1;'>Quizzes Created</p>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>99.2%</h2>
            <p style='color:#cbd5e1;'>Uptime Guaranteed</p>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>180+</h2>
            <p style='color:#cbd5e1;'>Countries Served</p>
        """, unsafe_allow_html=True)

        
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds cd0b | © 2025'
        '</div>', 
        unsafe_allow_html=True
    )

def show_generate_quiz():
       

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

    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff; margin-bottom: 2rem;'>🧠 Learning Buddy</h2>", unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content','👤 profile', '⚙️ Settings']
        
        for page in pages:
            if st.button(page, key=page, use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]

    col1, col2 = st.columns([4,1])
    
    with col1:
        st.markdown('<div class="welcome-header" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Generate New Quiz</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Create a customized quiz based on your preferences.</div>', unsafe_allow_html=True)
        
    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'
    
    st.session_state.setdefault("quiz_count", 0)
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("user_email", None)
    
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "show_answers" not in st.session_state:
        st.session_state.show_answers = False
    if "attempted_quizzes" not in st.session_state:
        st.session_state.attempted_quizzes = []
    with st.form("quiz_form"):
        topic = st.text_input("Topic or Concept", placeholder="e.g., Percentages")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("Number of Questions", 1, 10, 3)
        submit = st.form_submit_button("Generate Quiz")

    if submit:
        with st.spinner("Generating quiz..."):
            try:
                quiz_data = generate_quiz(topic, "Multiple Choice", difficulty, num_questions)
                st.session_state.quiz_data = quiz_data
                st.session_state.user_answers = {}
                st.session_state.show_answers = False
                st.success("✅ Quiz generated successfully!")
            except Exception as e:
                st.error(f"❌ Quiz generation failed: {e}")

    if st.session_state.get("quiz_data"):
        st.subheader("📝 Quiz Time")
        for idx, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"<div style='color: white; font-size: 1.1rem; font-weight: 600;'>Q{idx+1}: {q['question']}</div>", unsafe_allow_html=True)
            st.session_state.user_answers[idx] = st.radio(
                f"Choose your answer (Q{idx+1})",
                q["options"],
                key=f"q_{idx}",
                index=None
            )
            st.markdown("---")

        if st.button("Submit Answers"):
            score = 0
            total = len(st.session_state.quiz_data)
            for idx, q in enumerate(st.session_state.quiz_data):
                if st.session_state.user_answers.get(idx) == q["correct_answer"]:
                    score += 1

            percentage = (score / total) * 100
            st.success(f"✅ You scored {score}/{total} ({percentage:.2f}%)")

            # Show explanations after result
            st.subheader("🧠 Explanation for Each Question")
            for idx, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(idx)
                correct = q["correct_answer"]
                color = "green" if user_ans == correct else "red"
                st.markdown(f"""
                    <div style='border:1px solid #ccc; border-radius:10px; padding:1rem; margin-bottom:1rem; background-color:#1e293b;'>
                        <div style='font-weight:bold; color:white;'>Q{idx+1}: {q['question']}</div>
                        <div style='margin-top:0.5rem; color: {color};'><strong>Your Answer:</strong> {user_ans or "Not Answered"}</div>
                        <div style='color: #10b981;'><strong>Correct Answer:</strong> {correct}</div>
                        <div style='color: white; margin-top:0.5rem;'><strong>Explanation:</strong> {q['explanation']}</div>
                    </div>
                """, unsafe_allow_html=True)

            # Store the attempt in DB
            if 'user_id' in st.session_state and 'user_email' in st.session_state:
                try:
                    conn = get_connection()
                    cur = conn.cursor()

                    cur.execute("""
                        INSERT INTO quiz_attempts (
                            user_id, user_email, topic, qtype, difficulty,
                            score, percentage, attempted_at, questions, answers
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        st.session_state.user_id,
                        st.session_state.user_email,       # ✅ include user_email here
                        topic,
                        "Multiple Choice",
                        difficulty,
                        f"{score}/{total}",
                        f"{percentage:.2f}%",
                        datetime.now(),
                        json.dumps(st.session_state.quiz_data),
                        json.dumps(st.session_state.user_answers)
                    ))

                    conn.commit()
                    cur.close()
                    conn.close()
                    st.session_state.quiz_count += 1
                except Exception as e:
                    st.warning(f"⚠️ Error saving quiz attempt: {e}")

        
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 AI Quiz Generator - Powered by Advanced AI | © 2024'
        '</div>', 
        unsafe_allow_html=True
    )

import re

def remove_emojis(text):
    # Removes emojis and non-ASCII characters
    return re.sub(r'[^\x00-\x7F]+', '', text)

def export_styled_flashcards_pdf(cards, include_summary=True):
    if not cards:
        raise ValueError("No cards provided to export.")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(30, 30, 30)

    first = cards[0]

    if "node" in first:
        # ✅ MIND MAP FORMAT
        root = remove_emojis(first["node"])
        pdf.cell(0, 10, f"Mind Map: {root}", ln=True, align='C')
        pdf.ln(10)

        if "children" in first:
            for idx, child in enumerate(first["children"], 1):
                pdf.set_font("Arial", 'B', 14)
                pdf.set_text_color(0, 102, 204)
                pdf.cell(0, 10, f"{idx}. {remove_emojis(child['node'])}", ln=True)

                pdf.set_font("Arial", '', 12)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 8, f"Content: {remove_emojis(child['content'])}")
                pdf.ln(1)

                if include_summary and child.get("summary"):
                    pdf.set_font("Arial", 'I', 11)
                    pdf.set_text_color(100, 100, 100)
                    pdf.multi_cell(0, 8, f"Summary: {remove_emojis(child['summary'])}")
                    pdf.ln(2)

                pdf.ln(2)

        else:
            # Just root-level flashcard (no children)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, f"Content: {remove_emojis(first.get('content', ''))}")
            if include_summary and first.get("summary"):
                pdf.set_font("Arial", 'I', 11)
                pdf.multi_cell(0, 8, f"Summary: {remove_emojis(first['summary'])}")

    elif "question" in first and "answer" in first:
        # ✅ SINGLE FLASHCARD FORMAT
        pdf.cell(0, 10, "Flashcard", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 102, 204)
        pdf.multi_cell(0, 10, f"Question: {remove_emojis(first['question'])}")
        pdf.ln(5)

        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 8, f"Answer: {remove_emojis(first['answer'])}")
        pdf.ln(5)

        if include_summary and first.get("summary"):
            pdf.set_font("Arial", 'I', 11)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 8, f"Summary: {remove_emojis(first['summary'])}")
            pdf.ln(2)

    else:
        raise ValueError("Unrecognized flashcard format for PDF export.")

    filename = f"flashcards_{uuid.uuid4().hex[:8]}.pdf"
    pdf.output(filename)
    return filename
import uuid  # add at top if not present

def build_mindmap_html(node, include_summaries, prefix="node"):
    html_parts = []
    node_id = f"{prefix}-{uuid.uuid4().hex[:6]}"

    label = html.escape(node.get("node", node.get("question", "")))
    content = html.escape(node.get("content", node.get("answer", "")))
    summary = html.escape(node.get("summary", ""))

    html_parts.append(f"""
        <div class="arrow-line"></div>
        <div class="arrow-down"></div>
        <div class="child-node" onclick="showContent('{node_id}')">{label}</div>
        <div id="{node_id}" class="node-content" style="display:none;">
            <strong>📖 Content:</strong> {content}<br>
            {"<em>💡 Summary:</em> " + summary if include_summaries and summary else ""}
        </div>
    """)

    if "children" in node:
        for i, child in enumerate(node["children"]):
            html_parts.append(build_mindmap_html(child, include_summaries, f"{prefix}-{i}"))

    return "\n".join(html_parts)


def show_flashcards():
       

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
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    if 'generated_flashcards' not in st.session_state:
        st.session_state.generated_flashcards = []
    if 'include_summaries' not in st.session_state:
        st.session_state.include_summaries = True

    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff; margin-bottom: 2rem;'>🧠 Learning Buddy</h2>", unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content', '👤 profile', '⚙️ Settings']
        
        for page in pages:
            if st.button(page, key=page, use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]

    col1, col2 = st.columns([4,1])
    
    with col1:
        st.markdown('<div class="welcome-header" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Flashcards</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Review and practice with interactive flashcards.</div>', unsafe_allow_html=True)
        
    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'
    # Flashcard form
    with st.form("flashcard_form"):
        text = st.text_area("Enter your source material:", height=150)
        col1, col2 = st.columns(2)
        
        with col1:
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        include_summaries = st.toggle("Include Summaries", value=True)
        submitted = st.form_submit_button("Generate Content")

        if submitted:
            with st.spinner("Generating content for you..."):
                try:
                    cards = generate_flashcards(text, difficulty, include_summaries)
                    st.session_state.generated_flashcards = cards
                    st.session_state.include_summaries = include_summaries
                    st.success(f"{len(cards)} flashcards generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    cards = st.session_state.generated_flashcards
    include_summaries = st.session_state.include_summaries

    if cards:
        if cards:
            first = cards[0]

            if "node" in first:
                st.markdown(f"<div class='section-header'> {first['node']}</div>", unsafe_allow_html=True)
                if first.get("content"):
                    st.info(first["content"])

                for idx, child in enumerate(first.get("children", [])):
                    key = f"show_child_{idx}"
                    with st.expander(f"🔹 {child['node']}", expanded=st.session_state.get(key, False)):
                        st.session_state[key] = True  # Mark as opened
                        st.markdown(f"""
                            <div style="background:#1e293b;padding:1rem;border-radius:10px;">
                                <strong style="color:white;">📘 Content:</strong> <span style="color:#e2e8f0;">{child['content']}</span><br><br>
                                {"<strong style='color:white;'>💡 Summary:</strong> <em style='color:#a5f3fc;'>" + child['summary'] + "</em>" if include_summaries and child.get('summary') else ""}
                            </div>
                        """, unsafe_allow_html=True)

            elif "question" in first and "answer" in first:
                st.markdown(f"<div class='section-header'>🧠 Flashcard: {first['question']}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background:#1e293b;padding:1.5rem;border-radius:10px;color:white'>
                        <strong>📘 Answer:</strong> {first['answer']}<br><br>
                        {"<em>💡 Summary:</em> " + first.get("summary", "") if include_summaries and first.get("summary") else ""}
                    </div>
                """, unsafe_allow_html=True)

            else:
                st.warning("⚠️ Unrecognized flashcard format.")


        # ✅ PDF Download
        try:
            pdf_path = export_styled_flashcards_pdf(cards, include_summaries)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download Flashcards (PDF)",
                    data=f.read(),
                    file_name="flashcards.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ PDF Export Failed: {e}")
        
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds cd0b | © 2025'
        '</div>', 
        unsafe_allow_html=True
    ) 

def show_saved_content():
       

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
        st.markdown("<h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff; margin-bottom: 2rem;'>🧠 Learning Buddy</h2>", unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content','👤 profile', '⚙️ Settings']
        
        for page in pages:
            if st.button(page, key=page, use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]

    col1, col2 = st.columns([4, 1])
   
    with col1:
        st.markdown('<div class="welcome-header" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Saved Quizzes</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Review your previously attempted quizzes here.</div>', unsafe_allow_html=True)

    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'
    # ✅ Debug: Show current user
    user_email = st.session_state.get("user_email", None)
    if user_email:
        st.info(f"📧 Logged in as: `{user_email}`")
    else:
        st.warning("⚠️ You are not logged in. Showing saved quizzes is only available for logged-in users.")
        return

    # ✅ Manual Save Button (only if last_attempt exists)
    if 'last_attempt' in st.session_state:
        if st.button("💾 Save Last Attempt to Database"):
            try:
                conn = get_connection()
                save_quiz_attempt(conn, user_email, st.session_state.last_attempt)
                conn.close()
                st.success("✅ Quiz attempt saved to database!")
                del st.session_state.last_attempt
            except Exception as e:
                st.error(f"❌ Failed to save quiz: {e}")

    # ✅ Fetch saved attempts
    conn = get_connection()
    attempts = get_attempts_for_user(conn, user_email)
    conn.close()

    if not attempts:
        st.info("❗ No quizzes attempted yet for this user.")
        return

    # ✅ Show all saved quizzes (with safety for missing questions)
    for i, quiz in enumerate(attempts):
        questions = quiz.get('questions')
        if not questions:
            st.warning(f"⚠️ Attempt {i+1} has no questions. Skipping.")
            continue

        with st.expander(f"📘 Attempt {i+1}: {quiz['topic']} | {quiz['type']} | {quiz['difficulty']} | Score: {quiz['score']}"):
            st.markdown(f"**📝 Topic:** {quiz['topic']}")
            st.markdown(f"**📚 Type:** {quiz['type']}")
            st.markdown(f"**🎯 Difficulty:** {quiz['difficulty']}")
            st.markdown(f"**🏆 Score:** {quiz['score']} ({quiz['percentage']})")
            st.markdown(f"**🕒 Attempted At:** {quiz['attempted_at'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown("---")

            for idx, q in enumerate(questions):
                user_ans = quiz.get('answers', {}).get(str(idx), "Not Answered")
                correct_ans = q.get("correct_answer", "N/A")
                question_text = q.get("question", "Missing question text")
                explanation = q.get("explanation", "No explanation available")
                result = "✅ Correct!" if user_ans == correct_ans else "❌ Incorrect"

                with st.container():
                    st.markdown(f"**Q{idx+1}:** {question_text}")
                    st.markdown(f"- **Your Answer:** {user_ans}")
                    st.markdown(f"- **Correct Answer:** {correct_ans}")
                    st.markdown(f"- **Result:** {result}")
                    st.markdown(f"- **Explanation:** {explanation}")
                    st.markdown("---")
        
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds cd0b | © 2025'
        '</div>', 
        unsafe_allow_html=True
    )

def show_profile():
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
        st.markdown("<h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff; margin-bottom: 2rem;'>🧠 Learning Buddy</h2>", unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content', '👤 profile', '⚙️ Settings']
        
        for page in pages:
            if st.button(page, key=page, use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]
   
    # Initialize defaults
    st.session_state.setdefault("quiz_count", 0)
    st.session_state.setdefault("study_streak", 0)
    st.session_state.setdefault("Friends", 0)
    st.session_state.setdefault("user_id", None)

    # Fetch data
    if st.session_state.user_id:
        try:
            conn = get_connection()
            cur = conn.cursor()
            uid = st.session_state.user_id

            cur.execute("SELECT study_streak, last_login_date FROM users WHERE id = %s", (uid,))
            result = cur.fetchone()
            today = datetime.now().date()

            if result:
                streak, last_login = result
                if last_login != today:
                    streak = streak + 1 if last_login == today - timedelta(days=1) else 1
                    cur.execute("UPDATE users SET study_streak=%s, last_login_date=%s WHERE id=%s", (streak, today, uid))
                    conn.commit()
                st.session_state.study_streak = streak

            cur.execute(
                "SELECT COUNT(*) FROM quiz_attempts WHERE user_id=%s AND attempted_at >= %s",
                (uid, today - timedelta(days=30))
            )
            st.session_state.quiz_count = cur.fetchone()[0]


            cur.execute("SELECT COUNT(*) FROM users")
            st.session_state.Friends = cur.fetchone()[0]
            cur.close()
            conn.close()
        except Exception as e:
            st.warning(f"Error fetching user data: {e}")


    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'
    st.markdown("<div class='section-header' style='color:#ffffff; text-shadow: 0 0 10px #C66727;'>📊 Your Study Insights</div>", unsafe_allow_html=True)

    col1, col2= st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Quizzes Completed</div>
            <div class="metric-number">{st.session_state.quiz_count}</div>
            <div class="metric-sublabel">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card-green">
            <div class="metric-label">Study Streak</div>
            <div class="metric-number">{st.session_state.study_streak}</div>
            <div class="metric-sublabel">Consecutive Days</div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    # The actual button
    with col1:
        clicked = st.button("👥 Friends", key="friends_card_button", use_container_width=True)
        st.markdown("""
                    <style>
                    /* Target the button created with key="friends_card_button" */
                    div[data-testid="element-container"] button[kind="secondary"] {
                        background: linear-gradient(135deg, #ea580c 0%, #f97316 100%) !important;
                        color: white !important;
                        border: none !important;
                        padding: 1.5rem !important;
                        border-radius: 12px !important;
                        font-size: 1.1rem !important;
                        font-weight: bold !important;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
                        transition: all 0.2s ease;
                    }

                    div[data-testid="element-container"] button[kind="secondary"]:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
                        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%) !important;
                    }
                    </style>
                """, unsafe_allow_html=True)              
        # Handle navigation
        if clicked:
            st.session_state.current_page = "Friends"
            st.rerun() 
        # --- UI Metrics ---
        
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds cd0b | © 2025'
        '</div>', 
        unsafe_allow_html=True
    )        

def show_settings():
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
        st.markdown("<h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff; margin-bottom: 2rem;'>🧠 Learning Buddy</h2>", unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '📝 Generate Quiz', '🎯 Flashcards', '💾 Saved Content', '👤 profile', '⚙️ Settings']
        
        for page in pages:
            if st.button(page, key=page, use_container_width=True):
                st.session_state.current_page = page.split(' ', 1)[1]

    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown('<div class="welcome-header" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Settings</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtext" style="color:#ffffff; text-shadow: 0 0 10px #C66727;">Configure your quiz preferences and account settings.</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("logout", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.signed_in = False
            st.session_state.current_page = 'Home'
    # Fetch password
    conn = get_connection()
    cur = conn.cursor()
    user_email = st.session_state.get("user_email", None)
    user_name = st.session_state.get("user_name", "")
    cur.execute("SELECT password FROM users WHERE email = %s", (user_email,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        st.error("User not found in the database.")
        return

    old_password = result[0]
    st.text_input("Full Name", user_name, disabled=True)
    st.text_input("Email", user_email, disabled=True)
    st.text_input("Old Password", value=old_password, key="old_password")

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if not new_password or not confirm_password:
            st.error("Please fill in all password fields.")
        elif new_password != confirm_password:
            st.error("New password and confirm password do not match.")
        else:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, user_email))
            conn.commit()
            cur.close()
            conn.close()
            st.success("Password updated successfully!")
                
        
        
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.9rem; padding: 1rem;">'
        '🧠 Learning Buddy - Powered by Bright Minds cd0b | © 2025'
        '</div>', 
        unsafe_allow_html=True
    )

