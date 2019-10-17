import os
import tempfile

import pytest

from app import create_app
from app.database import db
from app.models import User


@pytest.fixture
def client():
    app = create_app("testing")
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    db.app = app

    return client


@pytest.fixture
def user():
    return User.create(email="test@gmail.com")
