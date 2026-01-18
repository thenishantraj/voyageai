"""
Confidence Scoring Engine
Sophisticated algorithm for destination recommendations with confidence scores
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import random

@dataclass
class Destination:
    """Destination data structure"""
    id: str
    name: str
    country: str
    category: str
    description: str
    average_cost: float
    best_season: str
    travel_time: float
    highlights: List[str]
    weather_score: float
    crowd_score: float
    dna_affinity: Dict[str, float]  # Affinity scores for each travel dimension

class ConfidenceEngine:
    """Main engine for calculating confidence scores"""
    
    def __init__(self):
        self.season_weights = self._initialize_season_weights()
        self.category_affinities = self._initialize_category_affinities()
        
    def _initialize_season_weights(self) -> Dict[str, Dict[str, float]]:
        """Initialize season-based scoring weights"""
        return {
            "Spring": {"weather": 0.9, "crowd": 0.7, "cost": 0.6},
            "Summer": {"weather": 0.8, "crowd": 0.5, "cost": 0.4},
            "Fall": {"weather": 0.95, "crowd": 0.8, "cost": 0.7},
            "Winter": {"weather": 0.6, "crowd": 0.9, "cost": 0.8}
        }
    
    def _initialize_category_affinities(self) -> Dict[str, Dict[str, float]]:
        """Initialize category to DNA dimension affinities"""
        return {
            "Adventure": {"adventure": 0.9, "comfort": 0.2, "nature": 0.8},
            "Cultural": {"culture": 0.9, "urban": 0.7, "social": 0.6},
            "Luxury": {"luxury": 0.9, "comfort": 0.8, "adventure": 0.1},
            "Nature": {"nature": 0.9, "adventure": 0.6, "comfort": 0.4},
            "Urban": {"urban": 0.9, "culture": 0.7, "social": 0.8},
            "Beach": {"comfort": 0.9, "luxury": 0.6, "nature": 0.5},
            "Wellness": {"comfort": 0.9, "nature": 0.7, "luxury": 0.5}
        }
    
    def calculate_recommendations(self, destinations: List[Dict], 
                                 user_prefs: Dict) -> List[Dict]:
        """
        Calculate confidence-scored destination recommendations
        
        Args:
            destinations: List of destination dictionaries
            user_prefs: User preferences including travel DNA
            
        Returns:
            List of destinations with confidence scores
        """
        recommendations = []
        
        for dest in destinations:
            scores = self._calculate_individual_scores(dest, user_prefs)
            confidence_score = self._calculate_confidence_score(scores)
            
            recommendation = dest.copy()
            recommendation.update({
                "confidence_score": confidence_score,
                "budget_score": scores["budget_score"],
                "weather_score": scores["weather_score"],
                "crowd_score": scores["crowd_score"],
                "dna_match": scores["dna_match"],
                "breakdown": scores
            })
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_individual_scores(self, destination: Dict, 
                                   user_prefs: Dict) -> Dict[str, float]:
        """Calculate individual component scores"""
        scores = {}
        
        # Budget score (0-10)
        scores["budget_score"] = self._calculate_budget_score(
            destination["average_cost"], 
            user_prefs["budget_min"], 
            user_prefs["budget_max"]
        )
        
        # Weather score (0-10)
        scores["weather_score"] = self._calculate_weather_score(
            destination["weather_score"],
            user_prefs.get("weather_priority", 5),
            user_prefs.get("travel_dates", None)
        )
        
        # Crowd score (0-10)
        scores["crowd_score"] = self._calculate_crowd_score(
            destination["crowd_score"],
            user_prefs.get("crowd_tolerance", 5),
            user_prefs.get("travel_dates", None)
        )
        
        # DNA Match score (0-10)
        scores["dna_match"] = self._calculate_dna_match(
            destination,
            user_prefs.get("travel_dna", None)
        )
        
        # Category relevance (0-10)
        scores["category_score"] = self._calculate_category_score(
            destination["category"],
            user_prefs.get("interests", [])
        )
        
        # Seasonal optimization (0-10)
        scores["seasonal_score"] = self._calculate_seasonal_score(
            destination["best_season"],
            user_prefs.get("travel_dates", None)
        )
        
        return scores
    
    def _calculate_budget_score(self, destination_cost: float, 
                              user_min: float, user_max: float) -> float:
        """Calculate budget compatibility score"""
        if destination_cost <= user_min:
            return 8.0 + (2.0 * (destination_cost / user_min))
        elif destination_cost <= user_max:
            # Linear interpolation between min and max
            normalized = (destination_cost - user_min) / (user_max - user_min)
            return 10.0 - (normalized * 4.0)  # 10 at min, 6 at max
        else:
            # Exponential decay beyond max budget
            overshoot = destination_cost / user_max
            return max(0, 6.0 * (1.0 / overshoot))
    
    def _calculate_weather_score(self, dest_weather: float, 
                               user_priority: float, travel_dates: Any) -> float:
        """Calculate weather compatibility score"""
        base_score = dest_weather
        
        # Adjust based on user priority
        priority_factor = user_priority / 10.0
        adjusted_score = base_score * (0.5 + 0.5 * priority_factor)
        
        # Seasonal adjustment if dates provided
        if travel_dates:
            seasonal_boost = self._get_seasonal_boost(travel_dates)
            adjusted_score *= (0.7 + 0.3 * seasonal_boost)
        
        return min(10.0, adjusted_score)
    
    def _calculate_crowd_score(self, dest_crowd: float, 
                             user_tolerance: float, travel_dates: Any) -> float:
        """Calculate crowd compatibility score"""
        # Invert crowd score for destinations (lower crowds = higher score)
        inverted_crowd = 10.0 - dest_crowd
        
        # Match with user tolerance (5 = neutral)
        tolerance_factor = user_tolerance / 5.0
        if tolerance_factor <= 1.0:
            # Prefer lower crowds
            adjusted_score = inverted_crowd * (1.0 + (1.0 - tolerance_factor))
        else:
            # Prefer higher crowds
            adjusted_score = dest_crowd * (tolerance_factor - 1.0)
        
        return min(10.0, adjusted_score / 2.0)  # Normalize to 0-10
    
    def _calculate_dna_match(self, destination: Dict, 
                           travel_dna: Dict) -> float:
        """Calculate DNA compatibility score"""
        if not travel_dna:
            return 5.0  # Neutral score if no DNA profile
        
        dna_dimensions = travel_dna.get("dimensions", {})
        destination_affinity = destination.get("dna_affinity", {})
        
        if not destination_affinity:
            return 5.0
        
        # Calculate weighted match
        total_weight = 0
        weighted_sum = 0
        
        for dimension, user_score in dna_dimensions.items():
            if dimension in destination_affinity:
                dest_score = destination_affinity[dimension]
                similarity = 10.0 - abs(user_score - dest_score)
                weight = user_score / 10.0  # Weight by user's preference strength
                
                weighted_sum += similarity * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 5.0
    
    def _calculate_category_score(self, destination_category: str, 
                                user_interests: List[str]) -> float:
        """Calculate category relevance score"""
        category_mapping = {
            "Adventure": ["Adventure", "Mountains"],
            "Cultural": ["History", "Cities", "Culture"],
            "Luxury": ["Shopping", "Wellness"],
            "Nature": ["Beaches", "Mountains", "Nature"],
            "Urban": ["Cities", "Food", "Shopping"],
            "Beach": ["Beaches", "Wellness"],
            "Wellness": ["Wellness", "Nature"]
        }
        
        if not user_interests:
            return 5.0
        
        category_keywords = category_mapping.get(destination_category, [])
        matches = sum(1 for interest in user_interests 
                     if interest in category_keywords)
        
        return (matches / len(user_interests)) * 10.0 if user_interests else 5.0
    
    def _calculate_seasonal_score(self, best_season: str, 
                                travel_dates: Any) -> float:
        """Calculate seasonal optimization score"""
        if not travel_dates:
            return 5.0
        
        # Parse travel dates (assuming tuple of start and end)
        try:
            if isinstance(travel_dates, tuple) and len(travel_dates) >= 2:
                travel_month = travel_dates[0].month
            else:
                travel_month = datetime.now().month
        except:
            travel_month = datetime.now().month
        
        # Map months to seasons
        month_to_season = {
            12: "Winter", 1: "Winter", 2: "Winter",
            3: "Spring", 4: "Spring", 5: "Spring",
            6: "Summer", 7: "Summer", 8: "Summer",
            9: "Fall", 10: "Fall", 11: "Fall"
        }
        
        travel_season = month_to_season.get(travel_month, "Spring")
        
        # Score based on season match
        season_parts = [s.strip() for s in best_season.split(",")]
        if travel_season in season_parts:
            return 9.0
        elif any(s in season_parts for s in ["All", "Year-round"]):
            return 7.0
        else:
            # Adjacent seasons get moderate score
            season_order = ["Winter", "Spring", "Summer", "Fall"]
            travel_idx = season_order.index(travel_season)
            best_seasons_idx = [season_order.index(s) for s in season_parts if s in season_order]
            
            if best_seasons_idx:
                min_distance = min(abs(travel_idx - idx) for idx in best_seasons_idx)
                if min_distance == 1:
                    return 6.0
                else:
                    return 3.0
            return 5.0
    
    def _get_seasonal_boost(self, travel_dates: Any) -> float:
        """Get seasonal boost factor for scoring"""
        # Simplified: peak season = 0.8, shoulder = 1.0, off-season = 1.2
        try:
            if isinstance(travel_dates, tuple) and len(travel_dates) >= 2:
                month = travel_dates[0].month
            else:
                month = datetime.now().month
        except:
            month = datetime.now().month
        
        # Peak seasons (lower boost)
        peak_months = [6, 7, 8, 12]  # Summer and December
        # Shoulder seasons (neutral)
        shoulder_months = [4, 5, 9, 10, 11]
        # Off-season (higher boost)
        off_months = [1, 2, 3]
        
        if month in peak_months:
            return 0.8
        elif month in shoulder_months:
            return 1.0
        else:
            return 1.2
    
    def _calculate_confidence_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate final confidence score from component scores
        
        Uses weighted geometric mean to emphasize balanced performance
        """
        weights = {
            "budget_score": 0.25,      # Most important
            "dna_match": 0.20,         # Psychological fit
            "weather_score": 0.15,     # Environmental factors
            "crowd_score": 0.15,       # Social factors
            "category_score": 0.15,    # Interest alignment
            "seasonal_score": 0.10     # Timing optimization
        }
        
        # Ensure all required scores are present
        for key in weights:
            if key not in scores:
                scores[key] = 5.0  # Default neutral score
        
        # Calculate weighted geometric mean (penalizes low individual scores more)
        log_sum = 0
        weight_sum = 0
        
        for key, weight in weights.items():
            score = max(0.1, scores[key])  # Avoid log(0)
            log_sum += weight * np.log(score)
            weight_sum += weight
        
        geometric_mean = np.exp(log_sum / weight_sum)
        
        # Convert to 0-100 scale
        confidence_score = geometric_mean * 10
        
        # Apply non-linear scaling to create distinction
        confidence_score = self._apply_confidence_curve(confidence_score)
        
        return round(min(100, max(0, confidence_score)), 1)
    
    def _apply_confidence_curve(self, score: float) -> float:
        """
        Apply S-curve transformation to confidence scores
        
        Creates clearer distinction between good (70-85) and excellent (85-100) matches
        """
        if score >= 85:
            # Boost top scores slightly
            return score + (100 - score) * 0.3
        elif score >= 70:
            # Linear for good scores
            return score
        elif score >= 50:
            # Slight penalty for mediocre scores
            return score * 0.9
        else:
            # Strong penalty for poor matches
            return score * 0.7
    
    def get_recommendation_breakdown(self, destination: Dict, 
                                   user_prefs: Dict) -> Dict[str, Any]:
        """
        Get detailed breakdown of recommendation factors
        
        Useful for explainable AI and user understanding
        """
        scores = self._calculate_individual_scores(destination, user_prefs)
        confidence = self._calculate_confidence_score(scores)
        
        return {
            "confidence_score": confidence,
            "component_scores": scores,
            "primary_strengths": self._identify_strengths(scores),
            "potential_concerns": self._identify_concerns(scores, destination, user_prefs),
            "optimization_suggestions": self._generate_optimizations(scores, destination, user_prefs)
        }
    
    def _identify_strengths(self, scores: Dict[str, float]) -> List[str]:
        """Identify primary strengths based on scores"""
        strengths = []
        score_threshold = 8.0
        
        if scores.get("budget_score", 0) >= score_threshold:
            strengths.append("Excellent budget fit")
        if scores.get("dna_match", 0) >= score_threshold:
            strengths.append("Perfect personality match")
        if scores.get("weather_score", 0) >= score_threshold:
            strengths.append("Ideal weather conditions")
        if scores.get("category_score", 0) >= score_threshold:
            strengths.append("Matches your interests")
        
        return strengths
    
    def _identify_concerns(self, scores: Dict[str, float], 
                          destination: Dict, user_prefs: Dict) -> List[str]:
        """Identify potential concerns or trade-offs"""
        concerns = []
        concern_threshold = 4.0
        
        if scores.get("budget_score", 0) <= concern_threshold:
            concerns.append("May exceed your budget range")
        if scores.get("crowd_score", 0) <= concern_threshold:
            tolerance = user_prefs.get("crowd_tolerance", 5)
            if tolerance < 5:
                concerns.append("Potentially crowded during your travel dates")
            else:
                concerns.append("May be quieter than preferred")
        
        # Check for season mismatch
        if scores.get("seasonal_score", 0) <= concern_threshold:
            concerns.append("Not ideal season for this destination")
        
        return concerns
    
    def _generate_optimizations(self, scores: Dict[str, float], 
                              destination: Dict, user_prefs: Dict) -> List[str]:
        """Generate optimization suggestions"""
        optimizations = []
        
        # Budget optimizations
        if scores.get("budget_score", 0) < 7.0:
            cost = destination.get("average_cost", 0)
            budget_max = user_prefs.get("budget_max", 0)
            
            if cost > budget_max:
                savings_needed = cost - budget_max
                optimizations.append(
                    f"Consider traveling in shoulder season to save ~${savings_needed:.0f}"
                )
        
        # Timing optimizations
        if scores.get("seasonal_score", 0) < 7.0:
            best_season = destination.get("best_season", "")
            optimizations.append(
                f"For optimal experience, visit during {best_season}"
            )
        
        # Crowd optimizations
        if scores.get("crowd_score", 0) < 6.0:
            tolerance = user_prefs.get("crowd_tolerance", 5)
            if tolerance < 5:
                optimizations.append(
                    "Consider early morning visits to popular attractions"
                )
        
        return optimizations