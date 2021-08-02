import pytest
from flask import Flask

from flask_constance import Constance


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.testing = True
    Constance(app)
    with app.app_context():
        yield app
