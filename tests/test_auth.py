from uuid import uuid4
import json

from unittest import mock

from app.models import User


def test_sign_up_without_email(client):
    rv = client.post("/sign_up", content_type="application/json", data=json.dumps({}))
    json_data = rv.get_json()

    assert json_data["message"] == "The e-mail field is missing"
    assert rv.status_code == 422
    assert User.get_by(email=None) is None


@mock.patch("app.models.User.is_email_taken")
def test_sign_up_with_taken_email(mock_is_email_taken, client):
    mock_is_email_taken.return_value = True
    num_of_rows = User.query().filter_by(email="test@rb.com.br").count()

    rv = client.post(
        "/sign_up",
        content_type="application/json",
        data=json.dumps({"email": "test@rb.com.br"}),
    )
    json_data = rv.get_json()

    assert json_data["message"] == "This e-mail is already in use"
    assert rv.status_code == 422
    assert User.query().filter_by(email="test@rb.com.br").count() == num_of_rows


@mock.patch("app.auth.send_sign_up_mail")
def test_sign_up(mock_sign_up_mail, client, faker):
    email = faker.email()

    rv = client.post(
        "/sign_up", content_type="application/json", data=json.dumps({"email": email})
    )
    json_data = rv.get_json()

    assert "user" in json_data
    assert json_data["user"]["email"] == email
    assert rv.status_code == 201
    assert User.get_by(email=email) is not None
    assert mock_sign_up_mail.call_count == 1


def test_get_user_with_invalid_id(client):
    id = uuid4()

    rv = client.get("/users/" + str(id))
    json_data = rv.get_json()

    assert json_data["message"] == "This id is not associated to a user"
    assert rv.status_code == 404


def test_get_user(user, client):
    id = user.id

    rv = client.get("/users/" + str(id))
    json_data = rv.get_json()

    assert "user" in json_data

    rv_user = json_data["user"]

    assert rv_user["id"] == str(user.id)
    assert rv_user["email"] == user.email
    assert rv_user["ranking"] == user.ranking
