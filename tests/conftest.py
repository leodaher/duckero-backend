import os
import tempfile
from random import randint, seed

import pytest
from faker import Faker

from app import create_app
from app.database import db
from app.models import User


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def client():
    app = create_app("testing")
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    db.app = app

    return client


@pytest.fixture
def user(faker):
    seed()
    subscribers = randint(0, 10)
    return User.create(email=faker.email(), subscribers=subscribers)
