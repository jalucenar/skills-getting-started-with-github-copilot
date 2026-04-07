def test_get_activities_returns_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert "description" in data[expected_activity]
    assert "participants" in data[expected_activity]
    assert isinstance(data[expected_activity]["participants"], list)


def test_signup_adds_new_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    activity_response = client.get("/activities")
    assert email in activity_response.json()[activity]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"

    # Act
    first_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    second_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"]


def test_remove_participant_unregisters_student(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

    activity_response = client.get("/activities")
    assert email not in activity_response.json()[activity]["participants"]


def test_remove_missing_participant_returns_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"{email} is not signed up for {activity}"
