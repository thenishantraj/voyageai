# 🧭 VoyageAI: Discover with Confidence

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://voyageai.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Travel search is not a technical problem; it's a psychological one."** > VoyageAI is a next-generation decision-support platform designed for **VOYAGEHACK 3.0** to eliminate travel decision anxiety.

---

## 🚀 The Problem & Our Vision

Modern travel platforms overwhelm users with endless options, leading to **Decision Fatigue** and **Booking Anxiety**. Travelers don't want more search results; they want the *confidence* to decide.

**VoyageAI** shifts the focus from "Search" to "Discovery" by:
1. Understanding the traveler's **Psychological DNA**.
2. Calculating a multi-factor **Confidence Score**.
3. Providing **AI-Powered Justifications** to build trust.

---

## ✨ Key Features

### 🧬 Travel DNA Profiling
Using a custom **Centroid-based Classification Algorithm**, we map users across 7 psychological dimensions (Adventure, Comfort, Culture, Luxury, Nature, Urban, Social) through an interactive assessment.

### 🎯 Confidence Scoring Engine
Our proprietary scoring model uses a **Weighted Geometric Mean** to evaluate:
- **Budget Fit (25%)**: Dynamic compatibility with user spending limits.
- **DNA Match (20%)**: Psychological alignment with the destination's vibe.
- **Environmental Factors (30%)**: Real-time weather and crowd density optimization.
- **Interest Alignment (25%)**: Synergy with user-selected travel categories.

### 🤖 Explainable AI (XAI)
Integrated with **Google Gemini-1.5-Flash**, the platform generates:
- **Personalized Justifications**: Why a specific trip is perfect for *you*.
- **Regret Previews**: Proactive management of trade-offs to ensure post-booking satisfaction.

### 🎨 Premium Glassmorphism UI
A high-performance interface built with Streamlit and custom CSS, featuring smooth animations and a professional fintech-grade aesthetic.

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit, Custom CSS3 (Glassmorphism)
- **Backend:** Python 3.x
- **Machine Learning:** Scikit-learn (Euclidean Distance / Centroid Matching)
- **Generative AI:** Google Gemini API (via `google-generativeai`)
- **Data Visualization:** Plotly, Pillow
- **Data Handling:** Pandas, NumPy

---

## 📁 Project Structure

```text
voyageai/
├── app.py                
├── styles.css            
├── src/
│   ├── travel_dna.py     
│   ├── recommendation.py 
│   ├── gemini_client.py  
│   └── synthetic_data.py 
└── .streamlit/
    └── config.toml       
