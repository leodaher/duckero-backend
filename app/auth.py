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

    rv = jsonify(
        {"user": {"id": user.id, "email": user.email, "ranking": user.ranking}}
    )
    rv.status_code = 201
    return rv


@auth_api.route("/users/<id>")
def get_user(id):
    user = User.get_by(id=id)

    if user is None:
        rv = jsonify({"message": "This id is not associated to a user"})
        rv.status_code = 404
        return rv

    rv = jsonify(
        {"user": {"id": user.id, "email": user.email, "ranking": user.ranking}}
    )
    rv.status_code = 200
    return rv
