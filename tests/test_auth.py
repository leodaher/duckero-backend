import json

from jwt import ExpiredSignatureError, InvalidTokenError
from unittest import mock

from app.models import User
from app.auth import encode_auth_token, decode_auth_token


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


def test_sign_up(client):

    rv = client.post(
        "/sign_up",
        content_type="application/json",
        data=json.dumps({"email": "test@rb.com.br"}),
    )
    json_data = rv.get_json()

    assert "token" in json_data
    assert "user" in json_data
    assert json_data["user"]["email"] == "test@rb.com.br"
    assert rv.status_code == 201
    assert User.get_by(email="test@rb.com.br") is not None


def test_verify_token_without_token(client):

    rv = client.post("/verify_token")
    json_data = rv.get_json()

    assert "message" in json_data
    assert json_data["message"] == "User is not authenticated"
    assert rv.status_code == 403


@mock.patch("app.auth.decode_auth_token")
def test_verify_token_with_expired_token(mock_decode_token, client):
    token = "token123"
    mock_decode_token.side_effect = ExpiredSignatureError

    rv = client.post("/verify_token", headers={"Authorization": token})
    json_data = rv.get_json()

    assert "message" in json_data
    assert json_data["message"] == "Token has expired"
    assert rv.status_code == 403


@mock.patch("app.auth.decode_auth_token")
def test_verify_token_with_invalid_token(mock_decode_token, client):
    token = "token123"
    mock_decode_token.side_effect = InvalidTokenError

    rv = client.post("/verify_token", headers={"Authorization": token})
    json_data = rv.get_json()

    assert "message" in json_data
    assert json_data["message"] == "Token is invalid"
    assert rv.status_code == 403


def test_encode_auth_token(user):
    token = encode_auth_token(str(user.id))

    assert token is not None


def test_decode_auth_token(user):
    token = encode_auth_token(str(user.id))

    user_id = decode_auth_token(token)

    assert user_id == str(user.id)
