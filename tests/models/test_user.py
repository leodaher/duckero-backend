from app.models import User


def test_init(faker):
    email = faker.email()

    user = User(email=email)

    assert user.email == email


def test_is_email_taken_with_already_in_use_email(user):

    rv = User.is_email_taken(user.email)

    assert rv == True


def test_is_email_taken_with_unused_email(faker):
    email = faker.email()

    rv = User.is_email_taken(email)

    assert rv == False
