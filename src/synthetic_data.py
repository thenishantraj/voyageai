"""
Synthetic Destination Dataset
Comprehensive dataset of 25+ global destinations with detailed attributes
"""

import random
from typing import List, Dict, Any
from datetime import datetime

DESTINATION_CATEGORIES = [
    "Adventure", "Cultural", "Luxury", "Nature", 
    "Urban", "Beach", "Wellness"
]

def generate_destinations() -> List[Dict]:
    """Generate synthetic dataset of global destinations"""
    
    destinations = [
        # Adventure Destinations
        {
            "id": "queenstown_nz",
            "name": "Queenstown",
            "country": "New Zealand",
            "category": "Adventure",
            "description": "World's adventure capital with bungee jumping, skiing, and stunning Southern Alps scenery.",
            "average_cost": 3500,
            "best_season": "Spring, Summer, Fall",
            "travel_time": 18,
            "highlights": ["Bungee Jumping", "Milford Sound", "Ski Resorts", "Wine Tours"],
            "weather_score": 7.5,
            "crowd_score": 6.8,
            "dna_affinity": {"adventure": 9.2, "nature": 8.5, "comfort": 6.0, "luxury": 5.5}
        },
        {
            "id": "interlaken_ch",
            "name": "Interlaken",
            "country": "Switzerland",
            "category": "Adventure",
            "description": "Alpine paradise between two lakes, offering paragliding, skiing, and mountain expeditions.",
            "average_cost": 4200,
            "best_season": "Summer, Winter",
            "travel_time": 12,
            "highlights": ["Jungfrau Region", "Paragliding", "Lake Thun", "Winter Sports"],
            "weather_score": 7.0,
            "crowd_score": 7.2,
            "dna_affinity": {"adventure": 8.8, "nature": 9.0, "comfort": 7.5, "luxury": 6.0}
        },
        
        # Cultural Destinations
        {
            "id": "kyoto_jp",
            "name": "Kyoto",
            "country": "Japan",
            "category": "Cultural",
            "description": "Ancient capital with 2000+ temples, traditional tea ceremonies, and seasonal beauty.",
            "average_cost": 3200,
            "best_season": "Spring, Fall",
            "travel_time": 14,
            "highlights": ["Golden Pavilion", "Geisha District", "Bamboo Forest", "Cherry Blossoms"],
            "weather_score": 8.0,
            "crowd_score": 8.5,
            "dna_affinity": {"culture": 9.5, "comfort": 8.0, "nature": 7.5, "urban": 6.5}
        },
        {
            "id": "rome_it",
            "name": "Rome",
            "country": "Italy",
            "category": "Cultural",
            "description": "Eternal city blending ancient history with vibrant modern life and culinary excellence.",
            "average_cost": 2800,
            "best_season": "Spring, Fall",
            "travel_time": 10,
            "highlights": ["Colosseum", "Vatican City", "Roman Forum", "Italian Cuisine"],
            "weather_score": 8.5,
            "crowd_score": 9.0,
            "dna_affinity": {"culture": 9.2, "urban": 8.0, "comfort": 7.0, "luxury": 6.8}
        },
        
        # Luxury Destinations
        {
            "id": "maldives",
            "name": "Maldives",
            "country": "Maldives",
            "category": "Luxury",
            "description": "Tropical paradise with overwater villas, crystal-clear lagoons, and exclusive resorts.",
            "average_cost": 8500,
            "best_season": "Winter, Spring",
            "travel_time": 20,
            "highlights": ["Overwater Bungalows", "Snorkeling", "Spa Retreats", "Private Islands"],
            "weather_score": 9.0,
            "crowd_score": 4.0,
            "dna_affinity": {"luxury": 9.8, "comfort": 9.5, "nature": 8.0, "adventure": 3.0}
        },
        {
            "id": "santorini_gr",
            "name": "Santorini",
            "country": "Greece",
            "category": "Luxury",
            "description": "Stunning volcanic island with white-washed buildings, sunset views, and premium amenities.",
            "average_cost": 4500,
            "best_season": "Spring, Summer, Fall",
            "travel_time": 15,
            "highlights": ["Caldera Views", "Wine Tasting", "Sunset Cruises", "Luxury Hotels"],
            "weather_score": 9.2,
            "crowd_score": 8.5,
            "dna_affinity": {"luxury": 9.0, "comfort": 8.8, "culture": 7.5, "nature": 6.5}
        },
        
        # Nature Destinations
        {
            "id": "banff_ca",
            "name": "Banff",
            "country": "Canada",
            "category": "Nature",
            "description": "Mountain wilderness in Canadian Rockies with turquoise lakes, glaciers, and wildlife.",
            "average_cost": 3000,
            "best_season": "Summer, Fall",
            "travel_time": 8,
            "highlights": ["Lake Louise", "Wildlife Viewing", "Hiking Trails", "Hot Springs"],
            "weather_score": 7.8,
            "crowd_score": 7.0,
            "dna_affinity": {"nature": 9.5, "adventure": 8.5, "comfort": 6.5, "luxury": 5.0}
        },
        {
            "id": "costa_rica",
            "name": "Costa Rica",
            "country": "Costa Rica",
            "category": "Nature",
            "description": "Biodiversity hotspot with rainforests, volcanoes, beaches, and eco-friendly tourism.",
            "average_cost": 2800,
            "best_season": "Winter, Spring",
            "travel_time": 6,
            "highlights": ["Arenal Volcano", "Monteverde Cloud Forest", "Wildlife Sanctuaries", "Eco-Lodges"],
            "weather_score": 8.5,
            "crowd_score": 6.5,
            "dna_affinity": {"nature": 9.3, "adventure": 8.0, "comfort": 7.0, "culture": 6.0}
        },
        
        # Urban Destinations
        {
            "id": "tokyo_jp",
            "name": "Tokyo",
            "country": "Japan",
            "category": "Urban",
            "description": "Ultra-modern metropolis blending cutting-edge technology with traditional culture.",
            "average_cost": 3800,
            "best_season": "Spring, Fall",
            "travel_time": 14,
            "highlights": ["Shibuya Crossing", "Tsukiji Market", "Traditional Temples", "Robot Restaurants"],
            "weather_score": 7.5,
            "crowd_score": 9.5,
            "dna_affinity": {"urban": 9.8, "culture": 8.5, "comfort": 8.0, "luxury": 7.5}
        },
        {
            "id": "new_york_us",
            "name": "New York City",
            "country": "USA",
            "category": "Urban",
            "description": "The city that never sleeps, with world-class museums, Broadway, and diverse neighborhoods.",
            "average_cost": 4200,
            "best_season": "Spring, Fall",
            "travel_time": 8,
            "highlights": ["Broadway Shows", "Central Park", "Metropolitan Museum", "Times Square"],
            "weather_score": 7.0,
            "crowd_score": 9.8,
            "dna_affinity": {"urban": 9.5, "culture": 9.0, "luxury": 8.0, "comfort": 7.0}
        },
        
        # Beach Destinations
        {
            "id": "bali_id",
            "name": "Bali",
            "country": "Indonesia",
            "category": "Beach",
            "description": "Island of gods with beautiful beaches, spiritual culture, and luxurious resorts.",
            "average_cost": 2500,
            "best_season": "Summer, Fall",
            "travel_time": 20,
            "highlights": ["Ubud Rice Terraces", "Beach Clubs", "Water Temples", "Surfing Spots"],
            "weather_score": 8.8,
            "crowd_score": 7.5,
            "dna_affinity": {"comfort": 8.5, "nature": 8.0, "culture": 7.5, "luxury": 7.0}
        },
        {
            "id": "tulum_mx",
            "name": "Tulum",
            "country": "Mexico",
            "category": "Beach",
            "description": "Bohemian beach town with Mayan ruins, cenotes, and eco-chic accommodations.",
            "average_cost": 2200,
            "best_season": "Winter, Spring",
            "travel_time": 5,
            "highlights": ["Mayan Ruins", "Cenotes", "Beach Clubs", "Eco-Resorts"],
            "weather_score": 9.0,
            "crowd_score": 7.0,
            "dna_affinity": {"comfort": 8.0, "nature": 8.5, "culture": 7.0, "adventure": 6.5}
        },
        
        # Wellness Destinations
        {
            "id": "ubud_id",
            "name": "Ubud",
            "country": "Indonesia",
            "category": "Wellness",
            "description": "Spiritual and wellness center in Bali with yoga retreats, healing centers, and organic cuisine.",
            "average_cost": 2000,
            "best_season": "Year-round",
            "travel_time": 20,
            "highlights": ["Yoga Retreats", "Organic Farms", "Healing Centers", "Monkey Forest"],
            "weather_score": 8.5,
            "crowd_score": 6.0,
            "dna_affinity": {"comfort": 9.0, "nature": 8.5, "culture": 7.0, "luxury": 6.0}
        },
        {
            "id": "sedona_us",
            "name": "Sedona",
            "country": "USA",
            "category": "Wellness",
            "description": "Desert town famous for red rock formations, spiritual energy vortices, and wellness retreats.",
            "average_cost": 1800,
            "best_season": "Spring, Fall",
            "travel_time": 4,
            "highlights": ["Vortex Sites", "Jeep Tours", "Spa Retreats", "Hiking Trails"],
            "weather_score": 8.0,
            "crowd_score": 5.5,
            "dna_affinity": {"comfort": 8.8, "nature": 8.5, "adventure": 7.0, "culture": 5.5}
        }
    ]
    
    # Add additional destinations for variety
    additional_destinations = [
        # More Adventure
        {
            "id": "cape_town_za",
            "name": "Cape Town",
            "country": "South Africa",
            "category": "Adventure",
            "description": "Coastal city with Table Mountain, wildlife safaris, and world-class vineyards.",
            "average_cost": 3200,
            "best_season": "Spring, Fall",
            "travel_time": 16,
            "highlights": ["Table Mountain", "Wine Lands", "Penguin Colony", "Safari Tours"],
            "weather_score": 8.5,
            "crowd_score": 6.5,
            "dna_affinity": {"adventure": 8.0, "nature": 8.5, "culture": 7.0, "luxury": 6.5}
        },
        
        # More Cultural
        {
            "id": "istanbul_tr",
            "name": "Istanbul",
            "country": "Turkey",
            "category": "Cultural",
            "description": "City straddling two continents with Byzantine and Ottoman heritage, bustling bazaars.",
            "average_cost": 1800,
            "best_season": "Spring, Fall",
            "travel_time": 12,
            "highlights": ["Hagia Sophia", "Grand Bazaar", "Bosphorus Cruise", "Turkish Baths"],
            "weather_score": 7.5,
            "crowd_score": 7.8,
            "dna_affinity": {"culture": 9.2, "urban": 8.0, "comfort": 6.5, "luxury": 5.5}
        },
        
        # More Luxury
        {
            "id": "dubai_ae",
            "name": "Dubai",
            "country": "UAE",
            "category": "Luxury",
            "description": "Ultra-modern city with luxury shopping, futuristic architecture, and desert adventures.",
            "average_cost": 5000,
            "best_season": "Winter, Spring",
            "travel_time": 14,
            "highlights": ["Burj Khalifa", "Luxury Malls", "Desert Safaris", "Palm Islands"],
            "weather_score": 8.0,
            "crowd_score": 7.0,
            "dna_affinity": {"luxury": 9.5, "urban": 8.5, "comfort": 8.0, "adventure": 6.0}
        },
        
        # More Nature
        {
            "id": "iceland",
            "name": "Iceland",
            "country": "Iceland",
            "category": "Nature",
            "description": "Land of fire and ice with glaciers, volcanoes, waterfalls, and Northern Lights.",
            "average_cost": 3800,
            "best_season": "Summer, Winter",
            "travel_time": 7,
            "highlights": ["Northern Lights", "Blue Lagoon", "Waterfalls", "Glacier Hiking"],
            "weather_score": 6.5,
            "crowd_score": 5.5,
            "dna_affinity": {"nature": 9.8, "adventure": 8.5, "comfort": 5.0, "luxury": 4.5}
        },
        
        # More Urban
        {
            "id": "london_uk",
            "name": "London",
            "country": "UK",
            "category": "Urban",
            "description": "Historic global capital with royal heritage, world-class museums, and diverse culture.",
            "average_cost": 3500,
            "best_season": "Spring, Summer, Fall",
            "travel_time": 8,
            "highlights": ["British Museum", "West End Shows", "Historical Sites", "Royal Parks"],
            "weather_score": 6.5,
            "crowd_score": 8.5,
            "dna_affinity": {"urban": 9.0, "culture": 9.2, "comfort": 7.5, "luxury": 7.0}
        }
    ]
    
    destinations.extend(additional_destinations)
    
    # Ensure all destinations have required fields
    for dest in destinations:
        if "dna_affinity" not in dest:
            dest["dna_affinity"] = {
                "adventure": random.uniform(3.0, 9.0),
                "comfort": random.uniform(3.0, 9.0),
                "culture": random.uniform(3.0, 9.0),
                "luxury": random.uniform(3.0, 9.0),
                "nature": random.uniform(3.0, 9.0),
                "urban": random.uniform(3.0, 9.0),
                "social": random.uniform(3.0, 9.0)
            }
    
    return destinations

def generate_destination_stats(destinations: List[Dict]) -> Dict[str, Any]:
    """Generate statistics about the destination dataset"""
    stats = {
        "total_destinations": len(destinations),
        "by_category": {},
        "avg_cost_by_category": {},
        "cost_range": {
            "min": float('inf'),
            "max": 0,
            "avg": 0
        }
    }
    
    total_cost = 0
    
    for dest in destinations:
        category = dest["category"]
        
        # Count by category
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        
        # Track cost range
        cost = dest["average_cost"]
        stats["cost_range"]["min"] = min(stats["cost_range"]["min"], cost)
        stats["cost_range"]["max"] = max(stats["cost_range"]["max"], cost)
        total_cost += cost
    
    stats["cost_range"]["avg"] = total_cost / len(destinations)
    
    # Calculate average cost by category
    category_costs = {}
    category_counts = {}
    
    for dest in destinations:
        category = dest["category"]
        category_costs[category] = category_costs.get(category, 0) + dest["average_cost"]
        category_counts[category] = category_counts.get(category, 0) + 1
    
    for category in category_costs:
        stats["avg_cost_by_category"][category] = category_costs[category] / category_counts[category]
    
    return stats