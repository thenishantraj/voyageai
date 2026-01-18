"""
Travel DNA Profiling System
Psychological profiling for travel personality classification
"""

import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class TravelPersonality(Enum):
    """Travel personality archetypes"""
    ADVENTURE_SEEKER = "Adventure Seeker"
    CULTURE_CONNOISSEUR = "Culture Connoisseur"
    LUXURY_ESCAPIST = "Luxury Escapist"
    NATURE_IMMERSER = "Nature Immerser"
    URBAN_EXPLORER = "Urban Explorer"
    RELAXATION_CHASER = "Relaxation Chaser"
    SOCIAL_CONNECTOR = "Social Connector"

TRAVEL_PERSONALITIES = {
    TravelPersonality.ADVENTURE_SEEKER: {
        "traits": "Thrill-seeking, Spontaneous, Risk-tolerant",
        "style": "Active exploration, off-the-beaten-path, physical challenges",
        "perfect_for": "Extreme sports, remote destinations, unpredictable itineraries"
    },
    TravelPersonality.CULTURE_CONNOISSEUR: {
        "traits": "Intellectual, Curious, Historically-minded",
        "style": "Museum-hopping, local immersion, culinary exploration",
        "perfect_for": "Historical sites, artistic hubs, traditional experiences"
    },
    TravelPersonality.LUXURY_ESCAPIST: {
        "traits": "Comfort-oriented, Quality-focused, Service-expecting",
        "style": "Premium accommodations, exclusive access, pampering services",
        "perfect_for": "5-star resorts, private tours, gourmet dining"
    },
    TravelPersonality.NATURE_IMMERSER: {
        "traits": "Eco-conscious, Peace-seeking, Nature-connected",
        "style": "Outdoor activities, wildlife watching, sustainable travel",
        "perfect_for": "National parks, eco-lodges, wilderness retreats"
    },
    TravelPersonality.URBAN_EXPLORER: {
        "traits": "Energy-seeking, Social, Trend-aware",
        "style": "City hopping, nightlife, modern architecture",
        "perfect_for": "Metropolitan cities, tech hubs, contemporary art scenes"
    },
    TravelPersonality.RELAXATION_CHASER: {
        "traits": "Calm, Rejuvenation-focused, Slow-paced",
        "style": "Beach lounging, spa retreats, minimal planning",
        "perfect_for": "Beach resorts, wellness retreats, countryside escapes"
    },
    TravelPersonality.SOCIAL_CONNECTOR: {
        "traits": "People-oriented, Communicative, Experience-sharing",
        "style": "Group tours, local interactions, social experiences",
        "perfect_for": "Festivals, community stays, shared accommodations"
    }
}

@dataclass
class DNAResponse:
    """Individual response from Travel DNA quiz"""
    question_id: str
    response: Any
    weight: float = 1.0
    dimension: str = None

class TravelDNAProfiler:
    """Psychological profiling engine for travel personalities"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
        self.personality_centroids = self._calculate_personality_centroids()
        
    def _initialize_questions(self) -> List[Dict]:
        """Initialize the psychological assessment questions"""
        return [
            {
                "id": "q1_adventure",
                "question": "When you hear 'vacation', what's your first instinct?",
                "type": "multiple_choice",
                "options": [
                    "Find the most thrilling activity available",
                    "Research historical and cultural sites",
                    "Book the most luxurious accommodation",
                    "Look for natural landscapes and wildlife",
                    "Explore city attractions and nightlife",
                    "Find the most relaxing beach or spa",
                    "Plan activities where I can meet new people"
                ],
                "dimensions": ["adventure", "culture", "luxury", "nature", "urban", "comfort", "social"]
            },
            {
                "id": "q2_budget",
                "question": "How do you typically allocate your travel budget?",
                "type": "multiple_choice",
                "options": [
                    "Experiences and adventures first",
                    "Museums, tours, and cultural activities",
                    "Premium accommodations and dining",
                    "Outdoor gear and park fees",
                    "Urban attractions and transportation",
                    "Comfort and relaxation services",
                    "Social activities and group experiences"
                ],
                "dimensions": ["adventure", "culture", "luxury", "nature", "urban", "comfort", "social"]
            },
            {
                "id": "q3_pace",
                "question": "What pace feels most natural for your travels?",
                "type": "slider",
                "range": [1, 10],
                "dimensions": ["adventure", "comfort"]
            },
            {
                "id": "q4_accommodation",
                "question": "Your ideal accommodation is...",
                "type": "multiple_choice",
                "options": [
                    "A base camp for daily adventures",
                    "Centrally located for cultural access",
                    "A 5-star resort with all amenities",
                    "An eco-lodge in nature",
                    "A trendy hotel in the city center",
                    "A quiet retreat with spa facilities",
                    "A social hostel or guesthouse"
                ],
                "dimensions": ["adventure", "culture", "luxury", "nature", "urban", "comfort", "social"]
            },
            {
                "id": "q5_planning",
                "question": "How structured do you prefer your itinerary?",
                "type": "slider",
                "range": [1, 10],
                "dimensions": ["adventure", "comfort"]
            },
            {
                "id": "q6_activities",
                "question": "Which activities excite you most?",
                "type": "selectbox",
                "options": [
                    "Hiking, rafting, or extreme sports",
                    "Museum visits and historical tours",
                    "Fine dining and luxury shopping",
                    "Wildlife safaris and nature walks",
                    "City tours and architectural sights",
                    "Spa treatments and beach lounging",
                    "Local festivals and social events"
                ],
                "dimensions": ["adventure", "culture", "luxury", "nature", "urban", "comfort", "social"]
            },
            {
                "id": "q7_social",
                "question": "How important are social interactions during travel?",
                "type": "slider",
                "range": [1, 10],
                "dimensions": ["social", "comfort"]
            },
            {
                "id": "q8_learning",
                "question": "What do you want to bring home from your travels?",
                "type": "multiple_choice",
                "options": [
                    "Adrenaline-filled memories",
                    "Cultural understanding and knowledge",
                    "Luxury experiences and photos",
                    "Connection with nature",
                    "Urban experiences and trends",
                    "Complete relaxation and rejuvenation",
                    "New friendships and connections"
                ],
                "dimensions": ["adventure", "culture", "luxury", "nature", "urban", "comfort", "social"]
            }
        ]
    
    def _calculate_personality_centroids(self) -> Dict[TravelPersonality, Dict[str, float]]:
        """Calculate psychological dimension centroids for each personality"""
        centroids = {
            TravelPersonality.ADVENTURE_SEEKER: {
                "adventure": 9.5, "comfort": 2.0, "culture": 4.0, 
                "luxury": 1.5, "nature": 7.0, "urban": 3.0, "social": 5.0
            },
            TravelPersonality.CULTURE_CONNOISSEUR: {
                "adventure": 3.0, "comfort": 5.0, "culture": 9.5,
                "luxury": 4.0, "nature": 4.0, "urban": 7.0, "social": 6.0
            },
            TravelPersonality.LUXURY_ESCAPIST: {
                "adventure": 1.5, "comfort": 9.5, "culture": 5.0,
                "luxury": 9.5, "nature": 3.0, "urban": 6.0, "social": 4.0
            },
            TravelPersonality.NATURE_IMMERSER: {
                "adventure": 6.0, "comfort": 4.0, "culture": 3.0,
                "luxury": 2.0, "nature": 9.5, "urban": 1.5, "social": 3.0
            },
            TravelPersonality.URBAN_EXPLORER: {
                "adventure": 4.0, "comfort": 6.0, "culture": 7.0,
                "luxury": 5.0, "nature": 2.0, "urban": 9.5, "social": 7.0
            },
            TravelPersonality.RELAXATION_CHASER: {
                "adventure": 1.5, "comfort": 9.5, "culture": 3.0,
                "luxury": 7.0, "nature": 6.0, "urban": 2.0, "social": 2.0
            },
            TravelPersonality.SOCIAL_CONNECTOR: {
                "adventure": 5.0, "comfort": 5.0, "culture": 6.0,
                "luxury": 3.0, "nature": 4.0, "urban": 7.0, "social": 9.5
            }
        }
        return centroids
    
    def get_quiz_questions(self) -> List[Dict]:
        """Get the quiz questions"""
        return self.questions
    
    def analyze_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze quiz responses and calculate travel DNA profile
        
        Args:
            responses: Dictionary of question_id to response
            
        Returns:
            Dictionary containing personality type and dimensions
        """
        # Map responses to psychological dimensions
        dimension_scores = {
            "adventure": 0, "comfort": 0, "culture": 0,
            "luxury": 0, "nature": 0, "urban": 0, "social": 0
        }
        
        response_count = {dim: 0 for dim in dimension_scores.keys()}
        
        for q_id, response in responses.items():
            # Find the question
            question = next((q for q in self.questions if q["id"] == q_id), None)
            if not question:
                continue
                
            dimensions = question.get("dimensions", [])
            
            if question["type"] == "multiple_choice":
                # Each option corresponds to a dimension
                option_idx = question["options"].index(response)
                if option_idx < len(dimensions):
                    dimension_scores[dimensions[option_idx]] += 9
                    response_count[dimensions[option_idx]] += 1
                    
            elif question["type"] == "slider":
                # Split between two dimensions
                if len(dimensions) == 2:
                    dim1, dim2 = dimensions
                    score = int(response)
                    dimension_scores[dim1] += score
                    dimension_scores[dim2] += (10 - score)
                    response_count[dim1] += 1
                    response_count[dim2] += 1
                    
            elif question["type"] == "selectbox":
                # Similar to multiple choice
                option_idx = question["options"].index(response)
                if option_idx < len(dimensions):
                    dimension_scores[dimensions[option_idx]] += 9
                    response_count[dimensions[option_idx]] += 1
        
        # Calculate average scores
        for dim in dimension_scores:
            if response_count[dim] > 0:
                dimension_scores[dim] = dimension_scores[dim] / response_count[dim]
        
        # Normalize scores to 0-10 scale
        max_score = max(dimension_scores.values()) if dimension_scores.values() else 1
        for dim in dimension_scores:
            dimension_scores[dim] = (dimension_scores[dim] / max_score) * 10
        
        # Find closest personality match
        personality_match = self._find_closest_personality(dimension_scores)
        
        # Calculate match percentage
        match_score = self._calculate_match_score(dimension_scores, personality_match)
        
        return {
            "personality_type": personality_match.value,
            "dimensions": dimension_scores,
            "match_score": match_score,
            "personality_details": TRAVEL_PERSONALITIES[personality_match]
        }
    
    def _find_closest_personality(self, user_dimensions: Dict[str, float]) -> TravelPersonality:
        """Find the closest personality match using Euclidean distance"""
        min_distance = float('inf')
        closest_personality = TravelPersonality.ADVENTURE_SEEKER
        
        for personality, centroid in self.personality_centroids.items():
            distance = 0
            for dim in user_dimensions:
                distance += (user_dimensions[dim] - centroid[dim]) ** 2
            distance = np.sqrt(distance)
            
            if distance < min_distance:
                min_distance = distance
                closest_personality = personality
        
        return closest_personality
    
    def _calculate_match_score(self, user_dimensions: Dict[str, float], 
                              personality: TravelPersonality) -> float:
        """Calculate match percentage (0-100)"""
        centroid = self.personality_centroids[personality]
        max_possible_distance = np.sqrt(len(user_dimensions) * (10 ** 2))
        
        distance = 0
        for dim in user_dimensions:
            distance += (user_dimensions[dim] - centroid[dim]) ** 2
        distance = np.sqrt(distance)
        
        match_percentage = max(0, 100 - (distance / max_possible_distance) * 100)
        return round(match_percentage, 1)
    
    def get_personality_insights(self, personality_type: TravelPersonality) -> Dict[str, str]:
        """Get detailed insights for a personality type"""
        return TRAVEL_PERSONALITIES.get(personality_type, {})