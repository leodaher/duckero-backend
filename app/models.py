from datetime import datetime
from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.database import BaseMixin, db
from app.utils import is_valid_uuid


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4, nullable=False
    )
    email = db.Column(db.String(), unique=True, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    subscribers = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email=None, ranking=None, clicks=0, subscribers=0, ref=None):
        self.email = email
        self.clicks = clicks
        self.subscribers = subscribers

        # Insert user in the last ranking
        if ranking is not None:
            self.ranking = ranking
        else:
            self.ranking = 1
            qv = User.query().order_by(desc(User.ranking)).limit(1)
            for user in qv:
                self.ranking = user.ranking + 1

        # Check if it was referenced from another user
        if ref is not None and is_valid_uuid(ref):
            user_ref = User.query().filter_by(id=ref).first()
            if user_ref is not None:
                user_ref.subscribers += 1
                user_ref.update_ranking()

    @property
    def score(self):
        # We use this to calculate how long the user has signed up
        dt = datetime.now()

        total_time = (dt - self.created_date).total_seconds()
        max_time = (dt - User.get_oldest_created_date()).total_seconds()
        normalized_time = total_time / max_time
        max_subscribers = User.get_max_subscribers()
        normalized_subscribers = self.subscribers / max_subscribers

        # This rule can be changed. We still need to find the best coefficients
        return 0.5 * normalized_time + 0.5 * normalized_subscribers

    def get_next_higher_ranking_user(self):
        """ Find the user with the next higher ranking than a user. """
        return User.get_by(ranking=self.ranking - 1)

    def update_ranking(self):
        """ Update the ranking of a user that had his link clicked. """
        next_user = self.get_next_higher_ranking_user()
        while next_user is not None and self.score > next_user.score:
            self.ranking -= 1
            next_user.ranking += 1
            next_user = self.get_next_higher_ranking_user()
        self.save()

    @classmethod
    def is_email_taken(cls, email):
        return User.query().filter_by(email=email).first() is not None

    @classmethod
    def get_oldest_created_date(cls):
        user = User.query().order_by(User.created_date).limit(1).one()
        return user.created_date if user else None

    @classmethod
    def get_max_subscribers(cls):
        user = User.query().order_by(desc(User.subscribers)).first()
        return user.subscribers

    def __repr__(self):
        return "<User id:{}>".format(self.id)

    def __str__(self):
        return "<User id:{} email:{} ranking:{}>".format(
            self.id, self.email, self.ranking
        )
