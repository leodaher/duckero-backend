from uuid import uuid4
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.database import BaseMixin, db
from app.utils import is_valid_uuid


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    ranking = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    subscribers = db.Column(db.Integer)
    link = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)

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
            user_ref = User.query().filter_by(link=ref).first()
            if user_ref is not None:
                user_ref.subscribers += 1

    @classmethod
    def is_email_taken(cls, email):
        return User.query().filter_by(email=email).first() is None

    def __repr__(self):
        return "<id {}>".format(self.id)

    def __str__(self):
        return "<User id:{} email:{} ranking:{}>".format(
            self.id, self.email, self.ranking
        )
