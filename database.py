"""
Database module for VoyageAI - User authentication and data persistence
"""

import sqlite3
import json
import hashlib
import os
from datetime import datetime
from typing import Optional, Dict, Any, List

DB_PATH = "voyageai.db"

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create user_profiles table (Travel DNA results)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            personality_type TEXT NOT NULL,
            match_score REAL,
            dimensions TEXT NOT NULL,  -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create user_preferences table (Quiz responses)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            responses TEXT NOT NULL,  -- JSON string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create saved_recommendations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recommendations TEXT NOT NULL,  -- JSON string
            preferences TEXT NOT NULL,  -- JSON string of trip preferences
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, email: str, password: str) -> bool:
    """Create a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user and return user data if successful"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        password_hash = hash_password(password)
        
        cursor.execute(
            "SELECT id, username, email, created_at FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                (user['id'],)
            )
            conn.commit()
            
            return dict(user)
        
        conn.close()
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None

def user_exists(username: str, email: str) -> bool:
    """Check if username or email already exists"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (username, email)
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False

def save_user_profile(user_id: int, personality_type: str, match_score: float, dimensions: Dict) -> bool:
    """Save user's Travel DNA profile"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO user_profiles (user_id, personality_type, match_score, dimensions) VALUES (?, ?, ?, ?)",
            (user_id, personality_type, match_score, json.dumps(dimensions))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving user profile: {e}")
        return False

def get_latest_user_profile(user_id: int) -> Optional[Dict]:
    """Get user's most recent Travel DNA profile"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM user_profiles WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (user_id,)
        )
        profile = cursor.fetchone()
        conn.close()
        
        if profile:
            profile = dict(profile)
            profile['dimensions'] = json.loads(profile['dimensions'])
            return profile
        return None
    except Exception as e:
        print(f"Error fetching user profile: {e}")
        return None

def save_user_preferences(user_id: int, responses: Dict) -> bool:
    """Save user's quiz responses"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO user_preferences (user_id, responses) VALUES (?, ?)",
            (user_id, json.dumps(responses))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving user preferences: {e}")
        return False

def get_latest_user_preferences(user_id: int) -> Optional[Dict]:
    """Get user's most recent quiz responses"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT responses FROM user_preferences WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (user_id,)
        )
        prefs = cursor.fetchone()
        conn.close()
        
        if prefs:
            return json.loads(prefs['responses'])
        return None
    except Exception as e:
        print(f"Error fetching user preferences: {e}")
        return None

def save_recommendations(user_id: int, recommendations: List, preferences: Dict) -> bool:
    """Save user's recommendations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO saved_recommendations (user_id, recommendations, preferences) VALUES (?, ?, ?)",
            (user_id, json.dumps(recommendations), json.dumps(preferences))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving recommendations: {e}")
        return False

def get_user_recommendations(user_id: int, limit: int = 5) -> List:
    """Get user's saved recommendations"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT recommendations, preferences, created_at FROM saved_recommendations WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        )
        recs = cursor.fetchall()
        conn.close()
        
        results = []
        for rec in recs:
            results.append({
                'recommendations': json.loads(rec['recommendations']),
                'preferences': json.loads(rec['preferences']),
                'created_at': rec['created_at']
            })
        return results
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

def delete_user_data(user_id: int) -> bool:
    """Delete all user data (for account deletion)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Foreign key cascade will handle related tables
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user data: {e}")
        return False

# Initialize database on module import
init_database()