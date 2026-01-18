"""
Utility functions for VoyageAI
"""

import streamlit as st
import pandas as pd
from typing import Any, Dict, List
import json
import base64

def load_css():
    """Load custom CSS from styles.css"""
    try:
        with open('styles.css', 'r') as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styles.")

def display_glass_card(title: str, content: str, height: str = "auto"):
    """Display a glassmorphism-styled card"""
    st.markdown(f"""
    <div class="glass-card" style="height: {height};">
        <div class="card-title">{title}</div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def format_currency(amount: float) -> str:
    """Format currency with proper symbols"""
    if amount >= 1000:
        return f"${amount:,.0f}"
    return f"${amount:,.2f}"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default value for zero denominator"""
    if denominator == 0:
        return default
    return numerator / denominator

def calculate_weighted_score(scores: Dict[str, float], 
                           weights: Dict[str, float]) -> float:
    """Calculate weighted score from component scores"""
    total_weight = sum(weights.values())
    weighted_sum = sum(scores.get(key, 0) * weight for key, weight in weights.items())
    
    if total_weight == 0:
        return 0.0
    
    return weighted_sum / total_weight

def create_confidence_gauge(score: float, label: str = "Confidence Score"):
    """Create a confidence score gauge visualization"""
    color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 60 else "#ef4444")
    
    html = f"""
    <div style="text-align: center; padding: 1rem;">
        <div style="
            width: 120px;
            height: 60px;
            margin: 0 auto;
            border-radius: 60px 60px 0 0;
            background: conic-gradient(
                {color} 0% {score}%, 
                #e5e7eb {score}% 100%
            );
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                width: 100px;
                height: 50px;
                background: white;
                border-radius: 50px 50px 0 0;
                bottom: 0;
                left: 10px;
            "></div>
        </div>
        <div style="font-size: 2rem; font-weight: 800; margin-top: 0.5rem; color: {color};">
            {score:.0f}%
        </div>
        <div style="font-size: 0.9rem; color: #6b7280;">
            {label}
        </div>
    </div>
    """
    
    return html

def get_season_from_date(date):
    """Get season from date"""
    month = date.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def validate_user_inputs(user_data: Dict) -> List[str]:
    """Validate user inputs and return list of errors"""
    errors = []
    
    # Budget validation
    if "budget_min" in user_data and "budget_max" in user_data:
        if user_data["budget_min"] > user_data["budget_max"]:
            errors.append("Minimum budget cannot exceed maximum budget")
        if user_data["budget_min"] < 0 or user_data["budget_max"] < 0:
            errors.append("Budget values must be positive")
    
    # Date validation
    if "travel_dates" in user_data and user_data["travel_dates"]:
        if isinstance(user_data["travel_dates"], tuple) and len(user_data["travel_dates"]) == 2:
            start_date, end_date = user_data["travel_dates"]
            if end_date < start_date:
                errors.append("End date cannot be before start date")
    
    return errors

def export_recommendations(recommendations: List[Dict], format: str = "json"):
    """Export recommendations in specified format"""
    if format == "json":
        return json.dumps(recommendations, indent=2)
    elif format == "csv":
        df = pd.DataFrame(recommendations)
        return df.to_csv(index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")

def get_image_base64(image_path: str) -> str:
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

def create_progress_bar(current: int, total: int, label: str = "Progress"):
    """Create a custom progress bar"""
    percentage = (current / total) * 100
    
    html = f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">{label}</span>
            <span>{current}/{total} ({percentage:.0f}%)</span>
        </div>
        <div style="
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                height: 100%;
                width: {percentage}%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 4px;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """
    
    return html

def handle_api_error(error: Exception, context: str = "") -> str:
    """Handle API errors gracefully"""
    error_messages = {
        "API key invalid": "Please check your API key configuration",
        "Rate limit exceeded": "API rate limit exceeded. Please try again later",
        "Network error": "Network connection issue. Please check your connection",
        "Service unavailable": "Service temporarily unavailable"
    }
    
    error_str = str(error).lower()
    
    for key, message in error_messages.items():
        if key.lower() in error_str:
            return f"{context}: {message}"
    
    return f"{context}: An unexpected error occurred. Please try again."