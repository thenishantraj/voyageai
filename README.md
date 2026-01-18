# 🧭 VoyageAI: Confidence-First Travel Discovery Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://voyageai.streamlit.app)
[![Built for VoyageHack 3.0](https://img.shields.io/badge/Hackathon-VoyageHack%203.0-blueviolet)](https://unstop.com/hackathons/voyagehack-30-tbo-1341050)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **"Traditional platforms show you where to search. VoyageAI helps you decide."** > VoyageAI is a psychologically-informed travel ecosystem built for **VOYAGEHACK 3.0** that eliminates decision anxiety through personalized Travel DNA profiling and multi-factor confidence scoring.

---

## 🎯 Project Vision
In a world of information overload, travelers are paralyzed by too many options. VoyageAI transforms the travel planning experience from a technical search problem into a psychological decision-support journey. By analyzing **7 psychological dimensions**, we build user confidence before they even hit 'Book'.

---

## ✨ Key Features

### 🧬 Travel DNA Profiling
- **Psychological Assessment**: An 8-question deep-dive into the user's travel psyche.
- **Archetype Mapping**: Classification into 7 distinct personalities (e.g., Adventure Seeker, Luxury Escapist).
- **Dimension Analysis**: 5-dimensional mapping of Adventure, Comfort, Culture, Luxury, and Nature.
- **Real-time Personalization**: Dynamic UI adjustments based on the user's unique DNA.

### 🎯 Confidence Scoring Engine
- **Multi-Factor Algorithm**: A sophisticated model weighing Budget, Weather, Crowds, and DNA Match.
- **Weighted Geometric Mean**: A balanced scoring system that penalizes poor-fit factors to ensure high-quality matches.
- **Timing Intelligence**: Seasonal optimization and real-time suitability analysis.
- **Explainable Metrics**: Complete transparency through detailed scoring breakdowns.

### 🤖 AI-Powered Explanations (XAI)
- **Personalized Justifications**: Integrated with **Google Gemini** to explain *why* a trip fits your specific DNA.
- **Regret Preview**: A unique feature that proactively manages trade-offs to reduce post-booking anxiety.
- **Comparative Intelligence**: Side-by-side psychological analysis of multiple destinations.

### 🎨 Premium User Experience
- **Glassmorphism Design**: A futuristic, semi-transparent UI inspired by high-end fintech apps.
- **Micro-Interactions**: Custom animations and smooth transitions using CSS3.
- **Responsive Layout**: A mobile-first, professional interface that works on any device.

---

## 🏗️ Technical Architecture



```text
voyageai/
├── app.py                # Main Orchestrator (Streamlit)
├── styles.css            # Glassmorphism Design System
├── requirements.txt      # Dependency Management
└── src/
    ├── travel_dna.py     # Psychological Profiling & Clustering
    ├── recommendation.py # Multi-Criteria Decision Engine
    ├── gemini_client.py  # LLM Integration & Prompt Engineering
    ├── synthetic_data.py # 25+ Global Destination Knowledge Base
    └── utils.py          # Visual Helpers & Data Formatting
