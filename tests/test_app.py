"""Tests for the Mergington High School Activities API"""

def test_get_activities(client):
    """Test GET /activities endpoint"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate(client):
    """Test signup fails when student already signed up"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    # Second signup with same email should fail
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup fails for non-existent activity"""
    response = client.post(
        "/activities/Fake%20Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # Signup first
    client.post("/activities/Chess%20Club/signup?email=unreg@mergington.edu")
    # Then unregister
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=unreg@mergington.edu"
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_unregister_not_signed_up(client):
    """Test unregister fails when student not signed up"""
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=notsignedup@mergington.edu"
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregister fails for non-existent activity"""
    response = client.delete(
        "/activities/Fake%20Club/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
