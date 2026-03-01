"""
Tests for the activity unregistration endpoint (DELETE /activities/{activity_name}/unregister).

This test module verifies that students can unregister from activities, with proper
validation for students not signed up and invalid activities.
"""


def test_unregister_success(client):
    """
    Test successful unregistration from an activity.
    
    A registered student should be able to unregister from an activity.
    
    Args:
        client: FastAPI TestClient fixture
    """
    # First, sign up a student
    signup_response = client.post(
        "/activities/Drama Club/signup",
        params={"email": "unregister_student@mergington.edu"}
    )
    assert signup_response.status_code == 200
    
    # Then unregister them
    response = client.delete(
        "/activities/Drama Club/unregister",
        params={"email": "unregister_student@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert "unregister_student@mergington.edu" in data["message"]
    
    # Verify the student is no longer in the participant list
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "unregister_student@mergington.edu" not in activities["Drama Club"]["participants"]


def test_unregister_existing_participant(client):
    """
    Test unregistering an existing participant from their activity.
    
    Michael is already registered for Chess Club and should be able to unregister.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify participant is removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    # Daniel should still be there
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_not_signed_up_student_returns_400(client):
    """
    Test that unregistering a student who is not signed up returns 400.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.delete(
        "/activities/Programming Class/unregister",
        params={"email": "notstudent@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"].lower()


def test_unregister_from_invalid_activity_returns_404(client):
    """
    Test that unregistering from a non-existent activity returns 404.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.delete(
        "/activities/Fake Club/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_unregister_twice_returns_400_on_second(client):
    """
    Test that unregistering twice returns an error on the second attempt.
    
    Args:
        client: FastAPI TestClient fixture
    """
    # Sign up a student
    signup_response = client.post(
        "/activities/Tennis Club/signup",
        params={"email": "double_unregister@mergington.edu"}
    )
    assert signup_response.status_code == 200
    
    # First unregister should succeed
    response1 = client.delete(
        "/activities/Tennis Club/unregister",
        params={"email": "double_unregister@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.delete(
        "/activities/Tennis Club/unregister",
        params={"email": "double_unregister@mergington.edu"}
    )
    assert response2.status_code == 400
    assert "not signed up" in response2.json()["detail"].lower()


def test_unregister_frees_up_spot_for_signup(client):
    """
    Test that unregistering allows another student to sign up.
    
    This verifies that the participant count is correctly decreased.
    
    Args:
        client: FastAPI TestClient fixture
    """
    activity = "Art Studio"
    student1 = "test_student1@mergington.edu"
    student2 = "test_student2@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Sign up first student
    client.post(f"/activities/{activity}/signup", params={"email": student1})
    
    # Verify count increased
    response_after_signup = client.get("/activities")
    after_signup_count = len(response_after_signup.json()[activity]["participants"])
    assert after_signup_count == initial_count + 1
    
    # Unregister first student
    client.delete(f"/activities/{activity}/unregister", params={"email": student1})
    
    # Verify count decreased back
    response_after_unregister = client.get("/activities")
    after_unregister_count = len(response_after_unregister.json()[activity]["participants"])
    assert after_unregister_count == initial_count
    
    # New student should now be able to sign up
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": student2})
    assert signup_response.status_code == 200
