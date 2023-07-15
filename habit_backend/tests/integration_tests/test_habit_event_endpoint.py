from app.schemas.habit_event import HabitEventRead


def test_habit_event_is_marked_as_completed(mock_application, habit_event_url, valid_user_id, valid_habit_id):
    body = {
        "user_id": valid_user_id,
        "habit_id": valid_habit_id
    }

    response = mock_application.post(url=habit_event_url, json=body)
    assert response.status_code == 201


def test_get_habit_event_by_id(mock_application, habit_event_get_by_id_url, valid_user_id, valid_habit_id):
    response = mock_application.get(url=habit_event_get_by_id_url)
    habit_event = HabitEventRead(**response.json())

    assert habit_event.user_id == valid_user_id
    assert habit_event.habit_id == valid_habit_id
    assert response.status_code == 200
