"""
Pytest configuration and shared fixtures for FastAPI integration tests.

This module provides:
- TestClient fixture for making HTTP requests to the FastAPI app
- Sample activities fixture with fresh test data for each test
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making HTTP requests to the FastAPI app.
    
    Returns:
        TestClient: Client configured for the app instance
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Provides a fresh copy of sample activities for testing.
    
    This fixture returns a dictionary of activities that matches the structure
    defined in src/app.py. Each test receives an independent copy to avoid
    test pollution.
    
    Returns:
        dict: Sample activities with 9 different extracurricular activities
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis training and friendly matches",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 16,
            "participants": ["christine@mergington.edu", "david@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater production and acting workshops",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture classes",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["james@mergington.edu", "mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking skills",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and STEM exploration",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        }
    }
