from app import app


def test_get_expenses():
    client = app.test_client()

    response = client.get("/expenses")

    assert response.status_code == 200


def test_create_expense():
    client = app.test_client()

    response = client.post(
        "/expenses",
        json={
            "title": "Test Coffee",
            "amount": 4.5,
            "category": "Food"
        }
    )

    assert response.status_code == 201


def test_get_single_expense():
    client = app.test_client()

    create_response = client.post(
        "/expenses",
        json={
            "title": "Test Coffee",
            "amount": 4.5,
            "category": "Food"
        }
    )

    expense_id = create_response.get_json()["id"]

    response = client.get(f"/expenses/{expense_id}")

    assert response.status_code == 200


def test_update_expense():
    client = app.test_client()

    create_response = client.post(
        "/expenses",
        json={
            "title": "Test Coffee",
            "amount": 4.5,
            "category": "Food"
        }
    )

    expense_id = create_response.get_json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={
            "title": "Updated Coffee",
            "amount": 5.0,
            "category": "Food"
        }
    )

    assert response.status_code == 200


def test_delete_expense():
    client = app.test_client()

    create_response = client.post(
        "/expenses",
        json={
            "title": "Test Coffee",
            "amount": 4.5,
            "category": "Food"
        }
    )

    expense_id = create_response.get_json()["id"]

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 200



def test_create_expense_missing_fields():
    client = app.test_client()

    response = client.post(
        "/expenses",
        json={"title": "Test Coffee"}
    )

    assert response.status_code == 400
    error = response.get_json()["error"]
    assert "amount" in error
    assert "category" in error


def test_update_expense_missing_fields():
    client = app.test_client()

    create_response = client.post(
        "/expenses",
        json={
            "title": "Test Coffee",
            "amount": 4.5,
            "category": "Food"
        }
    )

    expense_id = create_response.get_json()["id"]

    response = client.put(
        f"/expenses/{expense_id}",
        json={"title": "Updated Coffee"}
    )

    assert response.status_code == 400
    error = response.get_json()["error"]
    assert "amount" in error
    assert "category" in error

    client.delete(f"/expenses/{expense_id}")