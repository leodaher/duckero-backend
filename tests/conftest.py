import os
import tempfile

import pytest

from app import create_app
from app.database import db


@pytest.fixture
def client():
    app = create_app("testing")
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    client = app.test_client()

    with app.app_context():
        db.app = app

    yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
