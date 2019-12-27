from datetime import datetime

from freezegun import freeze_time
from sqlalchemy import desc
from unittest import mock

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


def test_get_oldest_created_date():
    expected_date = User.query().order_by(User.created_date).limit(1).one().created_date

    date = User.get_oldest_created_date()

    assert date == expected_date


def test_get_max_subscribers():
    expected = User.query().order_by(desc(User.subscribers)).first().subscribers

    subscribers = User.get_max_subscribers()

    assert subscribers == expected
    assert User.query().filter(User.subscribers > expected).first() is None


def test_get_next_higher_ranking_user(user):

    next_user = user.get_next_higher_ranking_user()

    assert next_user is not None
    assert next_user.ranking == user.ranking - 1


def test_get_next_higher_ranking_user_with_first_in_ranking(user):
    user.ranking = 1

    assert user.get_next_higher_ranking_user() is None


@freeze_time("2019-12-20")
@mock.patch(
    "app.models.User.get_oldest_created_date", return_value=datetime(2019, 12, 1)
)
@mock.patch("app.models.User.get_max_subscribers", return_value=10)
def test_score(mock_get_max_subs, mock_get_oldest, user):
    total_time = (datetime(2019, 12, 20) - user.created_date).total_seconds()
    max_time = (datetime(2019, 12, 20) - datetime(2019, 12, 1)).total_seconds()
    expected_score = 0.5 * (user.subscribers / 10) + 0.5 * (total_time / max_time)

    assert user.score == expected_score
    assert mock_get_max_subs.call_count == 1
    assert mock_get_oldest.call_count == 1


def test_update_ranking_without_next_user(user):
    user.ranking = 1

    user.update_ranking()

    assert user.get_next_higher_ranking_user() is None
    assert user.ranking == 1


def test_update_ranking_without_update(user, faker):
    next_user = user.get_next_higher_ranking_user()
    next_user.subscribers = user.subscribers + 10
    previous_ranking = user.ranking

    user.update_ranking()

    assert user.ranking == previous_ranking
    assert next_user.ranking == previous_ranking - 1


def test_update_ranking(user, faker):
    next_user = user.get_next_higher_ranking_user()
    user.subscribers = next_user.subscribers + 10
    previous_ranking = user.ranking

    user.update_ranking()

    assert user.ranking < previous_ranking
    assert next_user.ranking == previous_ranking
