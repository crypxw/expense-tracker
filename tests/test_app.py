from app import app


def test_get_expenses():
    client = app.test_client()

    response = client.get("/expenses")

    assert response.status_code == 200