import streamlit as st

def show_landing_page():
    

    # Inject Custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Initialize session states
    for key in ['show_signup', 'show_signin']:
        if key not in st.session_state:
            st.session_state[key] = False

    # Animated Background
    st.markdown('<div class="bg-animation"></div>', unsafe_allow_html=True)

    
    # ---------- Hero Section ----------
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content slide-in">
            <div class="hero-badge">🚀 Next-Generation AI Learning Platform</div>
            <h1 class="hero-title"  style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>Your Learning with Supercharged by AI</h1>
            <p class="hero-subtitle">Harness the power of advanced AI to create personalized, adaptive quizzes that boost engagement, improve retention, and deliver measurable learning outcomes.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # ---------- Header ----------
    spacer1, col1, col2, spacer2 = st.columns([3, 1, 1, 3])
    with col1:
        if st.button("🔑 Sign In", use_container_width=True):
            st.session_state.page = "signlog"
            st.rerun()
    with col2:
        if st.button("✨ Sign Up", use_container_width=True):
            st.session_state.page = "signlog"
            st.rerun()

    # ---------- Stats ----------
    
    st.markdown("""<div class="section-header fade-in"  style='text-align: center;'>
            <h2 class="section-title" style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>Powerful Features</h2>
            <p class="section-subtitle">Discover the comprehensive suite of tools designed to revolutionize your educational experience.</p>
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
        <h2 style='text-align: center; color: white; margin: 2rem 0; text-shadow: 0 0 10px #ffffff;'>🚀 Why Students Love Learning Buddy</h2>
        
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
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>25K+</h2>
            <p style='color:#cbd5e1;'>Active Educators</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>5M+</h2>
            <p style='color:#cbd5e1;'>Quizzes Created</p>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>99.2%</h2>
            <p style='color:#cbd5e1;'>Uptime Guaranteed</p>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <h2 style='color:#ffffff; text-shadow: 0 0 10px #ffffff;'>180+</h2>
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


if __name__ == "__main__":
    show_landing_page()
