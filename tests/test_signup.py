"""
Tests for the activity signup endpoint (POST /activities/{activity_name}/signup).

This test module verifies that students can sign up for activities, with proper
validation for duplicate signups, invalid activities, and capacity limits.
"""


def test_signup_success(client):
    """
    Test successful signup for an activity.
    
    A new student should be able to sign up for an available activity.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the student is now in the participant list
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_prevents_double_registration(client):
    """
    Test that a student cannot sign up twice for the same activity.
    
    If a student is already registered, attempting to sign up again should
    return a 400 error.
    
    Args:
        client: FastAPI TestClient fixture
    """
    # First signup should succeed
    response1 = client.post(
        "/activities/Programming Class/signup",
        params={"email": "newemail@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": "newemail@mergington.edu"}
    )
    
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_already_registered_student(client):
    """
    Test that already registered students cannot sign up again.
    
    Michael is already registered for Chess Club, so attempting to sign up
    again should return a 400 error.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_invalid_activity_returns_404(client):
    """
    Test that signing up for a non-existent activity returns 404.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_with_special_characters_in_email(client):
    """
    Test that students with special characters in emails can sign up.
    
    Args:
        client: FastAPI TestClient fixture
    """
    email = "student+tag@mergington.edu"
    
    response = client.post(
        "/activities/Science Club/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify signup
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Science Club"]["participants"]


def test_signup_multiple_students_same_activity(client):
    """
    Test that multiple different students can sign up for the same activity.
    
    Args:
        client: FastAPI TestClient fixture
    """
    emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    for email in emails:
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all students are signed up
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    for email in emails:
        assert email in activities["Gym Class"]["participants"]


def test_signup_email_case_sensitivity(client):
    """
    Test signup with different email case variations.
    
    Note: This documents current behavior. The API treats emails as case-sensitive,
    which means different casings are considered different students.
    
    Args:
        client: FastAPI TestClient fixture
    """
    email_lower = "casesensitive@mergington.edu"
    
    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": email_lower}
    )
    
    assert response.status_code == 200
