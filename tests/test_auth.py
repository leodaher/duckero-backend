import json

from unittest import mock

from app.models import User


@mock.patch("app.models.User.create")
def test_sign_up_without_email(mock_create_user, client):
    rv = client.post("/sign_up", content_type="application/json", data=json.dumps({}))
    json_data = rv.get_json()

    assert json_data["message"] == "The e-mail field is missing"
    assert rv.status_code == 422
    mock_create_user.assert_not_called()


def test_sign_up(client):
    # Little hack that allows us to check if the method was called
    User.create = mock.MagicMock(side_effect=User.create)

    rv = client.post(
        "/sign_up",
        content_type="application/json",
        data=json.dumps({"email": "test@rb.com.br"}),
    )
    json_data = rv.get_json()

    assert json_data["user"]["email"] == "test@rb.com.br"
    assert rv.status_code == 201
    User.create.assert_called_once()
