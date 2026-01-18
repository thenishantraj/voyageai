"""
Google Gemini API Integration
Generates personalized trip justifications and regret previews
"""

import google.generativeai as genai
import streamlit as st
from typing import Dict, Any, Optional
import json
import os

class GeminiExplainer:
    """AI-powered trip explanation generator using Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client"""
        self.api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
        
        if not self.api_key:
            st.warning("Gemini API key not found. Using mock explanations.")
            self.mock_mode = True
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.mock_mode = False
    
    def generate_trip_explanation(self, destination: Dict, 
                                user_profile: Dict, 
                                preferences: Dict) -> Dict[str, str]:
        """
        Generate AI-powered trip justification and regret preview
        
        Args:
            destination: Destination information
            user_profile: User's travel DNA profile
            preferences: User's quiz responses and preferences
            
        Returns:
            Dictionary with 'justification' and 'regret_preview'
        """
        if self.mock_mode:
            return self._generate_mock_explanation(destination, user_profile)
        
        try:
            prompt = self._build_explanation_prompt(destination, user_profile, preferences)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                return self._parse_gemini_response(response.text)
            else:
                return self._generate_mock_explanation(destination, user_profile)
                
        except Exception as e:
            st.error(f"AI explanation generation failed: {str(e)}")
            return self._generate_mock_explanation(destination, user_profile)
    
    def _build_explanation_prompt(self, destination: Dict, 
                                user_profile: Dict, 
                                preferences: Dict) -> str:
        """Build the prompt for Gemini"""
        personality = user_profile.get("personality_type", "Balanced Traveler") if user_profile else "Balanced Traveler"
        dimensions = user_profile.get("dimensions", {}) if user_profile else {}
        
        prompt = f"""
        You are a travel psychologist and expert trip planner for VoyageAI, a confidence-first travel platform.
        
        Generate TWO sections for a traveler with this profile:
        - Personality Type: {personality}
        - Key Traits: {json.dumps(dimensions, indent=2)}
        
        For this destination: {destination['name']}, {destination['country']}
        Category: {destination['category']}
        Description: {destination['description']}
        Highlights: {', '.join(destination['highlights'][:3])}
        
        SECTION 1: "Why This Trip?" - Generate a compelling, personalized justification (150-200 words) explaining why this destination perfectly matches their travel DNA. Focus on psychological fit, emotional benefits, and unique alignment with their personality.
        
        SECTION 2: "Regret Preview" - Honestly preview potential trade-offs or regrets (75-100 words) they might have, based on their personality and preferences. Be specific about what they might miss or find challenging.
        
        Format your response exactly as:
        JUSTIFICATION: [your text here]
        REGRET_PREVIEW: [your text here]
        
        Make it insightful, specific, and psychologically aware. Avoid generic travel advice.
        """
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, str]:
        """Parse Gemini response into structured format"""
        lines = response_text.strip().split('\n')
        
        justification = ""
        regret_preview = ""
        current_section = None
        
        for line in lines:
            if line.startswith("JUSTIFICATION:"):
                current_section = "justification"
                justification = line.replace("JUSTIFICATION:", "").strip()
            elif line.startswith("REGRET_PREVIEW:"):
                current_section = "regret_preview"
                regret_preview = line.replace("REGRET_PREVIEW:", "").strip()
            elif current_section == "justification":
                justification += " " + line.strip()
            elif current_section == "regret_preview":
                regret_preview += " " + line.strip()
        
        return {
            "justification": justification or "This destination aligns well with your travel personality and preferences.",
            "regret_preview": regret_preview or "Consider your tolerance for potential crowds or weather variations."
        }
    
    def _generate_mock_explanation(self, destination: Dict, 
                                 user_profile: Dict) -> Dict[str, str]:
        """Generate mock explanation when API is unavailable"""
        personality = user_profile.get("personality_type", "Traveler") if user_profile else "Traveler"
        
        # Mock justifications based on destination category
        category = destination.get("category", "").lower()
        
        justifications = {
            "adventure": f"As a {personality}, you thrive on new challenges and authentic experiences. {destination['name']} offers exactly that—opportunities to push your boundaries while connecting with spectacular natural environments. The unique activities here align with your desire for meaningful, excitement-filled journeys.",
            "cultural": f"Your {personality} profile shows deep curiosity about different ways of life. {destination['name']} provides rich cultural immersion through its history, traditions, and local interactions. This destination satisfies your intellectual curiosity while offering beautiful settings for reflection and learning.",
            "luxury": f"With your {personality} preferences, comfort and quality experiences matter most. {destination['name']} delivers exceptional service, refined amenities, and exclusive access that align perfectly with your travel values. You'll appreciate the attention to detail and opportunities for pampering.",
            "nature": f"Your {personality} traits indicate a strong connection to natural environments. {destination['name']} offers pristine landscapes, diverse ecosystems, and opportunities for environmental engagement that will deeply resonate with your values and rejuvenate your spirit.",
            "urban": f"As a {personality}, you enjoy vibrant energy and diverse experiences. {destination['name']} provides the perfect blend of cultural attractions, culinary scenes, and urban exploration that matches your pace and interests in contemporary experiences.",
            "beach": f"Your {personality} profile suggests you value relaxation and scenic beauty. {destination['name']} offers the ideal combination of stunning coastlines, comfortable accommodations, and opportunities for both activity and rest that align with your travel goals.",
            "wellness": f"With your {personality} preferences, rejuvenation and self-care are priorities. {destination['name']} provides holistic wellness experiences, peaceful environments, and activities focused on restoring balance—exactly what your travel DNA seeks for meaningful relaxation."
        }
        
        regret_previews = {
            "adventure": "If you prefer predictable itineraries and constant comforts, the physical demands and potential unpredictability might challenge your expectations. Consider your tolerance for rustic conditions.",
            "cultural": "If you primarily seek relaxation or nightlife, the focus on historical sites and cultural activities might feel too structured. The pace of exploration might overwhelm those wanting pure leisure.",
            "luxury": "Travelers seeking rugged authenticity or budget experiences might find the premium pricing and formal atmosphere less appealing than more casual destinations.",
            "nature": "Those craving urban excitement, nightlife, or constant connectivity might find the remote locations and limited amenities less satisfying than more developed destinations.",
            "urban": "If you seek solitude, natural quiet, or slow-paced relaxation, the city energy, noise, and constant stimulation might feel overwhelming rather than invigorating.",
            "beach": "Adventure-seekers or culture enthusiasts might find extended beach stays less stimulating than destinations offering more diverse activity options beyond coastal relaxation.",
            "wellness": "Travelers seeking high-energy activities, party scenes, or extensive sightseeing might find the wellness-focused pace and activities too gentle for their preferences."
        }
        
        default_category = "adventure"
        selected_category = category if category in justifications else default_category
        
        return {
            "justification": justifications.get(selected_category, justifications[default_category]),
            "regret_preview": regret_previews.get(selected_category, regret_previews[default_category])
        }
    
    def generate_trip_comparison(self, destination_a: Dict, 
                               destination_b: Dict, 
                               user_profile: Dict) -> str:
        """
        Generate comparison between two destinations
        
        Args:
            destination_a: First destination
            destination_b: Second destination
            user_profile: User's travel DNA
            
        Returns:
            Comparison analysis
        """
        if self.mock_mode:
            return self._generate_mock_comparison(destination_a, destination_b, user_profile)
        
        try:
            prompt = self._build_comparison_prompt(destination_a, destination_b, user_profile)
            response = self.model.generate_content(prompt)
            
            return response.text if response.text else self._generate_mock_comparison(destination_a, destination_b, user_profile)
            
        except Exception as e:
            st.error(f"AI comparison generation failed: {str(e)}")
            return self._generate_mock_comparison(destination_a, destination_b, user_profile)
    
    def _build_comparison_prompt(self, dest_a: Dict, dest_b: Dict, 
                               user_profile: Dict) -> str:
        """Build comparison prompt"""
        personality = user_profile.get("personality_type", "Traveler") if user_profile else "Traveler"
        
        return f"""
        Compare these two destinations for a traveler with {personality} personality:
        
        DESTINATION A: {dest_a['name']}, {dest_a['country']}
        Category: {dest_a['category']}
        Highlights: {', '.join(dest_a['highlights'][:3])}
        
        DESTINATION B: {dest_b['name']}, {dest_b['country']}
        Category: {dest_b['category']}
        Highlights: {', '.join(dest_b['highlights'][:3])}
        
        Provide a concise comparison (200-250 words) focusing on:
        1. Which better aligns with a {personality}'s psychological needs
        2. Key experiential differences
        3. Potential trade-offs for each option
        4. Situations where one clearly outperforms the other
        
        Be insightful and specific about psychological fit.
        """
    
    def _generate_mock_comparison(self, dest_a: Dict, dest_b: Dict, 
                                user_profile: Dict) -> str:
        """Generate mock comparison"""
        personality = user_profile.get("personality_type", "Traveler") if user_profile else "Traveler"
        
        return f"""
        For a {personality} traveler:
        
        {dest_a['name']} offers {dest_a['category'].lower()} experiences with focus on {dest_a['highlights'][0].lower()}. This destination provides structured opportunities that align with preferences for {personality.lower()} travel styles.
        
        {dest_b['name']} emphasizes {dest_b['category'].lower()} with highlights including {dest_b['highlights'][0].lower()}. This option might better suit those valuing {dest_b['category'].lower()} aspects of travel.
        
        The key difference lies in {dest_a['category']} versus {dest_b['category']} experiences. {dest_a['name']} tends toward more curated experiences, while {dest_b['name']} offers more spontaneous opportunities.
        
        Choose {dest_a['name']} if you prioritize {dest_a['category'].lower()} and structured discovery. Opt for {dest_b['name']} if you prefer {dest_b['category'].lower()} and flexible exploration.
        """