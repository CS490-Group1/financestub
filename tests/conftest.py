import pytest
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../api'))
sys.path.append(parent_dir)
from financestub import app as my_app

@pytest.fixture()
def app():
    app = my_app
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()