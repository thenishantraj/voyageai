"""
Authentication UI components for VoyageAI
"""

import streamlit as st
from datetime import datetime
import database as db

def render_login_signup():
    """Render login and signup forms"""
    
    # Initialize session state for auth
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    st.markdown("""
    <div class="auth-container" style="max-width: 400px; margin: 2rem auto;">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 class="gradient-text" style="font-size: 2.5rem;">✈️ VoyageAI</h1>
            <p style="color: #64748b;">Discover your next journey with confidence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle between login and signup
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True, 
                    type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'signup' else "secondary"):
            st.session_state.auth_mode = 'signup'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.auth_mode == 'login':
        render_login_form()
    else:
        render_signup_form()

def render_login_form():
    """Render login form"""
    with st.form("login_form"):
        st.markdown('<div class="glass-card" style="padding: 2rem;">', unsafe_allow_html=True)
        
        st.markdown("### Welcome Back! 👋")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields")
                return
            
            user = db.authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.user_id = user['id']
                st.session_state.username = user['username']
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid username or password")

def render_signup_form():
    """Render signup form"""
    with st.form("signup_form"):
        st.markdown('<div class="glass-card" style="padding: 2rem;">', unsafe_allow_html=True)
        
        st.markdown("### Create Your Account ✨")
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("✨ Sign Up", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill in all fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return
            
            if "@" not in email or "." not in email:
                st.error("Please enter a valid email address")
                return
            
            if db.user_exists(username, email):
                st.error("Username or email already exists")
                return
            
            if db.create_user(username, email, password):
                st.success("Account created successfully! Please log in.")
                st.session_state.auth_mode = 'login'
                st.rerun()
            else:
                st.error("Failed to create account. Please try again.")

def render_logout():
    """Render logout button in sidebar"""
    if st.session_state.get('authenticated', False):
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"### 👤 {st.session_state.username}")
            if st.button("🚪 Sign Out", use_container_width=True):
                # Clear all session state
                for key in ['authenticated', 'user', 'user_id', 'username', 
                           'quiz_completed', 'user_responses', 'current_step',
                           'show_recommendations']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

def check_authentication():
    """Check if user is authenticated, redirect to login if not"""
    if not st.session_state.get('authenticated', False):
        render_login_signup()
        return False
    return True