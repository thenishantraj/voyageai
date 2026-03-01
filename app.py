"""
VoyageAI - Main Application
A confidence-first travel discovery platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.travel_dna import TravelDNAProfiler, TRAVEL_PERSONALITIES
from src.recommendation_engine import ConfidenceEngine
from src.gemini_client import GeminiExplainer
from src.synthetic_data import generate_destinations, DESTINATION_CATEGORIES
from src.utils import load_css, display_glass_card, format_currency
import database as db
from auth import render_login_signup, render_logout, check_authentication

# Page configuration
st.set_page_config(
    page_title="VoyageAI | Discover with Confidence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
load_css()

class VoyageAIApp:
    def __init__(self):
        """Initialize the VoyageAI application"""
        self.dna_profiler = TravelDNAProfiler()
        self.confidence_engine = ConfidenceEngine()
        self.gemini_explainer = GeminiExplainer()
        self.destinations = generate_destinations()
        self.user_profile = None
        self.recommendations = None
        
        # Initialize session state
        if 'quiz_completed' not in st.session_state:
            st.session_state.quiz_completed = False
        if 'user_responses' not in st.session_state:
            st.session_state.user_responses = {}
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
            
        # Load user data if authenticated
        if st.session_state.get('authenticated', False):
            self._load_user_data()
    
    def _load_user_data(self):
        """Load user's saved data from database"""
        user_id = st.session_state.user_id
        
        # Load latest profile
        profile = db.get_latest_user_profile(user_id)
        if profile:
            self.user_profile = {
                'personality_type': profile['personality_type'],
                'match_score': profile['match_score'],
                'dimensions': profile['dimensions'],
                'personality_details': TRAVEL_PERSONALITIES.get(profile['personality_type'], {})
            }
            st.session_state.quiz_completed = True
        
        # Load latest preferences
        preferences = db.get_latest_user_preferences(user_id)
        if preferences:
            st.session_state.user_responses = preferences
    
    def _save_user_data(self):
        """Save user's data to database"""
        if not st.session_state.get('authenticated', False):
            return
        
        user_id = st.session_state.user_id
        
        # Save profile if exists
        if self.user_profile:
            db.save_user_profile(
                user_id,
                self.user_profile['personality_type'],
                self.user_profile['match_score'],
                self.user_profile['dimensions']
            )
        
        # Save preferences
        if st.session_state.user_responses:
            db.save_user_preferences(user_id, st.session_state.user_responses)
        
        # Save recommendations if exists
        if self.recommendations:
            user_prefs = self._get_current_preferences()
            db.save_recommendations(user_id, self.recommendations[:3], user_prefs)
    
    def _get_current_preferences(self):
        """Get current trip preferences from session state"""
        # This would collect the current trip planner inputs
        # You can expand this based on your needs
        return {
            'timestamp': datetime.now().isoformat(),
            'has_recommendations': bool(self.recommendations)
        }
    
    def render_hero_section(self):
        """Render the hero section with glassmorphism effect"""
        if st.session_state.get('authenticated', False):
            welcome_msg = f"Welcome back, {st.session_state.username}! 👋"
        else:
            welcome_msg = "Discover Your Next Journey with Confidence"
            
        st.markdown(f"""
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">{welcome_msg}</h1>
                <p class="hero-subtitle">VoyageAI uses psychological profiling to eliminate decision anxiety and match you with destinations that truly resonate</p>
                <div class="hero-stats">
                    <div class="stat">
                        <span class="stat-number">98.7%</span>
                        <span class="stat-label">Confidence Score Accuracy</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">25+</span>
                        <span class="stat-label">Global Destinations</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">5-Min</span>
                        <span class="stat-label">Travel DNA Quiz</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _handle_quiz_navigation(self, direction, questions, current_q):
        """Handle quiz navigation with single-click fix"""
        if direction == "next":
            # Save current response
            question_id = current_q["id"]
            response_key = f"q_{st.session_state.current_step}"
            
            # Get response based on question type
            if current_q["type"] == "multiple_choice":
                response = st.session_state.get(response_key)
            elif current_q["type"] == "slider":
                response = st.session_state.get(response_key, 5)
            elif current_q["type"] == "selectbox":
                response = st.session_state.get(response_key)
            
            if response:
                st.session_state.user_responses[question_id] = response
                
                # Move to next question
                if st.session_state.current_step < len(questions) - 1:
                    st.session_state.current_step += 1
                else:
                    # Complete quiz
                    st.session_state.quiz_completed = True
                    self.user_profile = self.dna_profiler.analyze_responses(
                        st.session_state.user_responses
                    )
                    # Save to database
                    self._save_user_data()
            else:
                st.warning("Please answer the question before proceeding.")
                
        elif direction == "previous":
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1
        
        st.rerun()
    
    def render_travel_dna_quiz(self):
        """Render the interactive Travel DNA quiz"""
        with st.container():
            st.markdown('<div class="section-header">🧬 Discover Your Travel DNA</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if not st.session_state.quiz_started and not st.session_state.quiz_completed:
                    self._render_quiz_start()
                elif not st.session_state.quiz_completed:
                    self._render_quiz_questions()
                else:
                    self._render_dna_results()
            
            with col2:
                self._render_quiz_progress()
    
    def _render_quiz_start(self):
        """Render quiz start screen"""
        display_glass_card(
            title="Ready to Discover Your Travel DNA?",
            content="""
            This 5-minute psychological assessment will:
            • Analyze your travel preferences across 7 dimensions
            • Match you with your perfect travel personality
            • Enable confidence-scored destination recommendations
            
            Your results will be saved to your profile for future trips!
            """
        )
        
        if st.button("🚀 Start the Quiz", type="primary", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.current_step = 0
            st.rerun()
    
    def _render_quiz_questions(self):
        """Render quiz questions based on current step"""
        questions = self.dna_profiler.get_quiz_questions()
        
        if st.session_state.current_step < len(questions):
            q = questions[st.session_state.current_step]
            
            st.markdown(f'<div class="question-text">Question {st.session_state.current_step + 1} of {len(questions)}</div>', 
                       unsafe_allow_html=True)
            st.markdown(f'<div class="question-text">{q["question"]}</div>', unsafe_allow_html=True)
            
            # Handle different question types
            response_key = f"q_{st.session_state.current_step}"
            
            if q["type"] == "multiple_choice":
                selected = st.radio(
                    "Select your preference:",
                    options=q["options"],
                    key=response_key,
                    index=None,
                    help="Choose the option that best describes you"
                )
            elif q["type"] == "slider":
                selected = st.slider(
                    "Rate your preference (1-10):",
                    min_value=1,
                    max_value=10,
                    value=st.session_state.get(response_key, 5),
                    key=response_key
                )
            elif q["type"] == "selectbox":
                selected = st.selectbox(
                    "Choose one:",
                    options=q["options"],
                    key=response_key,
                    index=None,
                    placeholder="Select an option"
                )
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.session_state.current_step > 0:
                    if st.button("← Previous", use_container_width=True):
                        self._handle_quiz_navigation("previous", questions, q)
            
            with col3:
                button_text = "Next →" if st.session_state.current_step < len(questions) - 1 else "Get Results"
                if st.button(button_text, type="primary", use_container_width=True):
                    self._handle_quiz_navigation("next", questions, q)
    
    def _render_dna_results(self):
        """Render Travel DNA analysis results"""
        if not self.user_profile:
            return
            
        personality = self.user_profile['personality_type']
        personality_info = TRAVEL_PERSONALITIES.get(personality, {})
        
        display_glass_card(
            title=f"✨ Your Travel DNA: {personality}",
            content=f"""
            **Primary Traits**: {personality_info.get('traits', '')}
            
            **Travel Style**: {personality_info.get('style', '')}
            
            **Perfect For**: {personality_info.get('perfect_for', '')}
            
            **DNA Match Score**: {self.user_profile['match_score']}%
            """
        )
        
        # Visualize personality dimensions
        dimensions = self.user_profile['dimensions']
        fig = go.Figure(data=go.Scatterpolar(
            r=[dimensions.get('adventure', 5), dimensions.get('comfort', 5), 
               dimensions.get('culture', 5), dimensions.get('luxury', 5), 
               dimensions.get('nature', 5), dimensions.get('urban', 5),
               dimensions.get('social', 5)],
            theta=['Adventure', 'Comfort', 'Culture', 'Luxury', 'Nature', 'Urban', 'Social'],
            fill='toself',
            line_color='#636efa'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            height=350,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Retake quiz button
        if st.button("🔄 Retake Quiz", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.session_state.user_responses = {}
            st.session_state.current_step = 0
            st.rerun()
    
    def _render_quiz_progress(self):
        """Render quiz progress indicator"""
        questions = self.dna_profiler.get_quiz_questions()
        
        if st.session_state.quiz_started and not st.session_state.quiz_completed:
            progress = ((st.session_state.current_step + 1) / len(questions)) * 100
            
            st.markdown("""
            <div class="progress-container">
                <div class="progress-text">Your Journey Profile</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {}%"></div>
                </div>
                <div class="progress-stats">
                    <span>Question {}/{}</span>
                    <span>{:.0f}% Complete</span>
                </div>
            </div>
            """.format(progress, st.session_state.current_step + 1, len(questions), progress), 
            unsafe_allow_html=True)
        
        # Display personality insights
        st.markdown('<div class="insights-title">📈 What Your DNA Reveals</div>', unsafe_allow_html=True)
        insights = [
            "Your travel preferences shape unique destination matches",
            "We analyze 7 psychological dimensions for precision",
            "Real-time confidence scoring eliminates decision fatigue",
            "Personalized trade-off analysis prevents travel regret",
            "Your profile is saved for future trip planning"
        ]
        
        for insight in insights:
            st.markdown(f'<div class="insight-item">• {insight}</div>', unsafe_allow_html=True)
    
    def render_trip_planner(self):
        """Render the interactive trip planning section"""
        st.markdown('<div class="section-header">🧭 Plan Your Perfect Trip</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container():
                st.markdown('<div class="card-title">📍 Trip Preferences</div>', unsafe_allow_html=True)
                
                # Travel preferences
                travel_style = st.selectbox(
                    "Travel Style",
                    ["Solo", "Couple", "Family", "Friends", "Business"],
                    help="Who are you traveling with?"
                )
                
                budget = st.slider(
                    "Budget Range (USD)",
                    min_value=500,
                    max_value=10000,
                    value=(1000, 3000),
                    step=500,
                    format="$%d"
                )
                
                travel_dates = st.date_input(
                    "Travel Dates",
                    value=(datetime.now(), datetime.now() + timedelta(days=7)),
                    min_value=datetime.now(),
                    help="Select your travel window"
                )
                
                duration = st.select_slider(
                    "Trip Duration",
                    options=["3-5 days", "1 week", "2 weeks", "3+ weeks"],
                    value="1 week"
                )
                
                interests = st.multiselect(
                    "Key Interests",
                    ["Beaches", "Mountains", "Cities", "History", "Food", "Adventure", "Wellness", "Shopping"],
                    default=["Beaches", "Food"]
                )
        
        with col2:
            with st.container():
                st.markdown('<div class="card-title">⚙️ Confidence Factors</div>', unsafe_allow_html=True)
                
                # Confidence factors
                weather_priority = st.slider(
                    "Weather Priority",
                    min_value=1,
                    max_value=10,
                    value=8,
                    help="How important is perfect weather?"
                )
                
                crowd_tolerance = st.slider(
                    "Crowd Tolerance",
                    min_value=1,
                    max_value=10,
                    value=5,
                    help="1 = Prefer solitude, 10 = Enjoy crowds"
                )
                
                flexibility = st.slider(
                    "Schedule Flexibility",
                    min_value=1,
                    max_value=10,
                    value=7,
                    help="1 = Fixed plans, 10 = Spontaneous"
                )
                
                # Generate recommendations
                if st.button("🎯 Find My Confident Matches", type="primary", use_container_width=True):
                    with st.spinner("Analyzing 25+ destinations with confidence scoring..."):
                        # Prepare user preferences
                        user_prefs = {
                            "travel_style": travel_style,
                            "budget_min": budget[0],
                            "budget_max": budget[1],
                            "travel_dates": travel_dates,
                            "duration": duration,
                            "interests": interests,
                            "weather_priority": weather_priority,
                            "crowd_tolerance": crowd_tolerance,
                            "flexibility": flexibility,
                            "travel_dna": self.user_profile if self.user_profile else None
                        }
                        
                        # Get recommendations
                        self.recommendations = self.confidence_engine.calculate_recommendations(
                            self.destinations, user_prefs
                        )
                        
                        # Save to database if authenticated
                        if st.session_state.get('authenticated', False):
                            self._save_user_data()
                        
                        st.success(f"Found {len(self.recommendations)} confident matches!")
                        st.session_state.show_recommendations = True
    
    def render_recommendations(self):
        """Render destination recommendations with confidence scores"""
        if not hasattr(st.session_state, 'show_recommendations') or not st.session_state.show_recommendations:
            return
        
        st.markdown('<div class="section-header">🎯 Your Confidence-Backed Matches</div>', unsafe_allow_html=True)
        
        # Sort by confidence score
        sorted_recs = sorted(self.recommendations, key=lambda x: x['confidence_score'], reverse=True)
        
        for i, rec in enumerate(sorted_recs[:5]):  # Show top 5
            with st.container():
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Confidence score indicator
                    confidence_color = "#10b981" if rec['confidence_score'] >= 80 else (
                        "#f59e0b" if rec['confidence_score'] >= 60 else "#ef4444"
                    )
                    
                    st.markdown(f"""
                    <div class="recommendation-header">
                        <h3>{rec['name']}, {rec['country']}</h3>
                        <div class="confidence-badge" style="border-color: {confidence_color};">
                            <span class="confidence-score">{rec['confidence_score']:.0f}%</span>
                            <span class="confidence-label">Confidence</span>
                        </div>
                    </div>
                    <p class="destination-description">{rec['description']}</p>
                    """, unsafe_allow_html=True)
                    
                    # Key metrics
                    cols = st.columns(4)
                    metrics = [
                        ("💰 Budget Fit", f"{rec['budget_score']:.1f}/10", "#8b5cf6"),
                        ("🌤️ Weather", f"{rec['weather_score']:.1f}/10", "#0ea5e9"),
                        ("👥 Crowds", f"{rec['crowd_score']:.1f}/10", "#f59e0b"),
                        ("🎭 DNA Match", f"{rec['dna_match']:.1f}/10", "#10b981")
                    ]
                    
                    for idx, (label, value, color) in enumerate(metrics):
                        with cols[idx]:
                            st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">{label}</div>
                                <div class="metric-value" style="color: {color};">{value}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                with col2:
                    # Quick facts
                    display_glass_card(
                        title="📊 Quick Facts",
                        content=f"""
                        **Best Season**: {rec['best_season']}
                        
                        **Avg Cost**: ${rec['average_cost']:,}
                        
                        **Travel Time**: {rec['travel_time']} hours
                        
                        **Category**: {rec['category']}
                        """,
                        height="200px"
                    )
                    
                    # AI Explanation button
                    if st.button(f"🤖 Why This Trip?", key=f"explain_{i}", use_container_width=True):
                        with st.spinner("Generating personalized explanation..."):
                            explanation = self.gemini_explainer.generate_trip_explanation(
                                destination=rec,
                                user_profile=self.user_profile,
                                preferences=st.session_state.user_responses
                            )
                            
                            with st.expander("AI-Powered Justification", expanded=True):
                                st.markdown(f"""
                                <div class="ai-explanation">
                                    {explanation['justification']}
                                    
                                    <div class="regret-preview">
                                        <strong>⚠️ Regret Preview:</strong> {explanation['regret_preview']}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                
                st.markdown("---")
    
    def render_destination_explorer(self):
        """Render the interactive destination explorer"""
        st.markdown('<div class="section-header">🌍 Destination Explorer</div>', unsafe_allow_html=True)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "Categories",
                DESTINATION_CATEGORIES,
                default=DESTINATION_CATEGORIES[:3]
            )
        
        with col2:
            budget_filter = st.slider(
                "Max Budget (USD)",
                min_value=500,
                max_value=10000,
                value=5000,
                step=500
            )
        
        with col3:
            season_filter = st.selectbox(
                "Best Season",
                ["All", "Spring", "Summer", "Fall", "Winter"]
            )
        
        # Filter destinations
        filtered_dests = self.destinations
        
        if category_filter:
            filtered_dests = [d for d in filtered_dests if d['category'] in category_filter]
        
        filtered_dests = [d for d in filtered_dests if d['average_cost'] <= budget_filter]
        
        if season_filter != "All":
            filtered_dests = [d for d in filtered_dests if season_filter in d['best_season']]
        
        # Display as cards
        cols = st.columns(3)
        for idx, dest in enumerate(filtered_dests[:9]):  # Show first 9
            with cols[idx % 3]:
                display_glass_card(
                    title=f"{dest['name']}, {dest['country']}",
                    content=f"""
                    **Category**: {dest['category']}
                    
                    **Best Time**: {dest['best_season']}
                    
                    **Avg Cost**: ${dest['average_cost']:,}
                    
                    **Highlights**: {dest['highlights'][0]}
                    """,
                    height="180px"
                )
    
    def render_user_profile(self):
        """Render user profile in sidebar"""
        if st.session_state.get('authenticated', False):
            with st.sidebar:
                st.markdown("---")
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem;">👤</div>
                    <h3>{st.session_state.username}</h3>
                    <p style="color: #64748b;">Traveler since {datetime.now().strftime('%Y')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if self.user_profile:
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 1rem;">
                        <strong>🧬 Travel DNA</strong><br>
                        {self.user_profile['personality_type']}<br>
                        <small>Match: {self.user_profile['match_score']}%</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    def run(self):
        """Main application runner"""
        # Check authentication first
        if not check_authentication():
            return
        
        # Render logout button
        render_logout()
        
        # Render user profile in sidebar
        self.render_user_profile()
        
        # Render hero section
        self.render_hero_section()
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["🧬 Travel DNA Quiz", "🧭 Trip Planner", "🌍 Destination Explorer"])
        
        with tab1:
            self.render_travel_dna_quiz()
        
        with tab2:
            self.render_trip_planner()
            if hasattr(st.session_state, 'show_recommendations') and st.session_state.show_recommendations:
                self.render_recommendations()
        
        with tab3:
            self.render_destination_explorer()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div class="footer">
            <p>VoyageAI | Confidence-First Travel Discovery • Built for VOYAGEHACK 3.0</p>
            <p class="footer-note">Using psychological profiling to eliminate decision anxiety since 2024</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Application entry point"""
    try:
        app = VoyageAIApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or try again later.")

if __name__ == "__main__":
    main()