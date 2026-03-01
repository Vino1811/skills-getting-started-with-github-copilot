"""
Tests for the activities listing endpoint (GET /activities).

This test module verifies that the API correctly returns all available activities
with the proper structure and data.
"""


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all available activities.
    
    Verifies that the endpoint returns a 200 status code and includes
    all 9 expected activities.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify all 9 activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Art Studio",
        "Debate Team",
        "Science Club"
    ]
    
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_returns_correct_structure(client):
    """
    Test that each activity has the correct structure.
    
    Each activity should have:
    - description: string
    - schedule: string
    - max_participants: integer
    - participants: list of email strings
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.get("/activities")
    activities = response.json()
    
    # Test the first activity as a sample
    chess_club = activities["Chess Club"]
    
    assert "description" in chess_club
    assert isinstance(chess_club["description"], str)
    assert len(chess_club["description"]) > 0
    
    assert "schedule" in chess_club
    assert isinstance(chess_club["schedule"], str)
    assert len(chess_club["schedule"]) > 0
    
    assert "max_participants" in chess_club
    assert isinstance(chess_club["max_participants"], int)
    assert chess_club["max_participants"] > 0
    
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_returns_participants_list(client):
    """
    Test that activities return their current participants.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club should have 2 participants initially
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Basketball Team should have 1 participant initially
    assert len(activities["Basketball Team"]["participants"]) == 1
    assert "alex@mergington.edu" in activities["Basketball Team"]["participants"]
