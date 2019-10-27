import datetime
import jwt

from flask import Blueprint, jsonify, request, current_app

from app.models import User

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json()

    # Check if email is in the body
    if "email" not in data:
        rv = jsonify({"message": "The e-mail field is missing"})
        rv.status_code = 422
        return rv

    if User.is_email_taken(data["email"]):
        rv = jsonify({"message": "This e-mail is already in use"})
        rv.status_code = 422
        return rv

    # Create and add user to database
    user = User.create(email=data["email"], ref=data.get("ref"))
    token = encode_auth_token(str(user.id))

    rv = jsonify(
        {
            "user": {"email": user.email, "ranking": user.ranking},
            "token": token.decode("utf-8"),
        }
    )
    rv.status_code = 201
    return rv


@auth_api.route("/verify_token", methods=["POST"])
def verify_token():
    token = request.headers.get("Authorization")

    if token is None:
        rv = jsonify({"message": "User is not authenticated"})
        rv.status_code = 403
        return rv

    try:
        user_id = decode_auth_token(token)
    except jwt.ExpiredSignatureError:
        rv = jsonify({"message": "Token has expired"})
        rv.status_code = 403
        return rv
    except jwt.InvalidTokenError:
        rv = jsonify({"message": "Token is invalid"})
        rv.status_code = 403
        return rv

    rv = jsonify({})
    rv.status_code = 200
    return rv


def encode_auth_token(user_id):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")


def decode_auth_token(auth_token):
    payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"))
    return payload["sub"]
