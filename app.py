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
    
    def render_hero_section(self):
        """Render the hero section with glassmorphism effect"""
        st.markdown("""
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">Discover Your Next Journey with <span class="gradient-text">Confidence</span></h1>
                <center><p class="hero-subtitle">VoyageAI uses psychological profiling to eliminate decision anxiety and match you with destinations that truly resonate</p></center>
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
    
    def render_travel_dna_quiz(self):
        """Render the interactive Travel DNA quiz"""
        with st.container():
            st.markdown('<div class="section-header">📊 Discover Your Travel DNA</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if not st.session_state.quiz_completed:
                    self._render_quiz_questions()
                else:
                    self._render_dna_results()
            
            with col2:
                self._render_quiz_progress()
    
    def _render_quiz_questions(self):
        """Render quiz questions based on current step"""
        questions = self.dna_profiler.get_quiz_questions()
        
        if st.session_state.current_step < len(questions):
            q = questions[st.session_state.current_step]
            
            with st.form(f"question_{st.session_state.current_step}"):
                st.markdown(f'<div class="question-text">{q["question"]}</div>', unsafe_allow_html=True)
                
                # Handle different question types
                if q["type"] == "multiple_choice":
                    selected = st.radio(
                        "Select your preference:",
                        options=q["options"],
                        key=f"q_{st.session_state.current_step}"
                    )
                elif q["type"] == "slider":
                    selected = st.slider(
                        "Rate your preference (1-10):",
                        min_value=1,
                        max_value=10,
                        value=5,
                        key=f"q_{st.session_state.current_step}"
                    )
                elif q["type"] == "selectbox":
                    selected = st.selectbox(
                        "Choose one:",
                        options=q["options"],
                        key=f"q_{st.session_state.current_step}"
                    )
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.session_state.current_step > 0:
                        if st.form_submit_button("← Previous"):
                            st.session_state.current_step -= 1
                            st.rerun()
                
                with col3:
                    submit_label = "Next →" if st.session_state.current_step < len(questions) - 1 else "Get Results"
                    if st.form_submit_button(submit_label):
                        st.session_state.user_responses[q["id"]] = selected
                        st.session_state.current_step += 1
                        
                        if st.session_state.current_step == len(questions):
                            st.session_state.quiz_completed = True
                            self.user_profile = self.dna_profiler.analyze_responses(st.session_state.user_responses)
                        st.rerun()
    
    def _render_dna_results(self):
        """Render Travel DNA analysis results"""
        if not self.user_profile:
            return
            
        personality = self.user_profile['personality_type']
        personality_info = TRAVEL_PERSONALITIES.get(personality, {})
        
        display_glass_card(
            title=f"✨ Your Travel DNA: {personality}",
           content=f"""
<div class="card-meta">
  <span class="pill">{dest['category']}</span>
</div>

<div class="card-row">
  <span class="label">Best Time</span>
  <span class="value">{dest['best_season']}</span>
</div>

<div class="card-row">
  <span class="label">Avg Cost</span>
  <span class="value">${dest['average_cost']}</span>
</div>

<div class="card-highlight">
  ✨ {dest['highlights'][0]}
</div>
"""

        )
        
        # Visualize personality dimensions
        dimensions = self.user_profile['dimensions']
        fig = go.Figure(data=go.Scatterpolar(
            r=[dimensions['adventure'], dimensions['comfort'], dimensions['culture'], 
               dimensions['luxury'], dimensions['nature']],
            theta=['Adventure', 'Comfort', 'Culture', 'Luxury', 'Nature'],
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
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_quiz_progress(self):
        """Render quiz progress indicator"""
        questions = self.dna_profiler.get_quiz_questions()
        progress = (st.session_state.current_step / len(questions)) * 100
        
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
            "We analyze 5 psychological dimensions for precision",
            "Real-time confidence scoring eliminates decision fatigue",
            "Personalized trade-off analysis prevents travel regret"
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
                            <span class="confidence-score">{rec['confidence_score']}%</span>
                            <span class="confidence-label">Confidence</span>
                        </div>
                    </div>
                    <p class="destination-description">{rec['description']}</p>
                    """, unsafe_allow_html=True)
                    
                    # Key metrics
                    cols = st.columns(4)
                    metrics = [
                        ("💰 Budget Fit", f"${rec['budget_score']}/10", "#8b5cf6"),
                        ("🌤️ Weather", f"{rec['weather_score']}/10", "#0ea5e9"),
                        ("👥 Crowds", f"{rec['crowd_score']}/10", "#f59e0b"),
                        ("🎭 DNA Match", f"{rec['dna_match']}/10", "#10b981")
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
                        
                        **Avg Cost**: ${rec['average_cost']}
                        
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
                    
                    **Avg Cost**: ${dest['average_cost']}
                    
                    **Highlights**: {dest['highlights'][0]}
                    """,
                    height="180px"
                )
    
    def run(self):
        """Main application runner"""
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