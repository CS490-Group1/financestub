'''
Conftest

Optional file. For now, not in use
'''
# pylint: disable=import-error, no-name-in-module
import sys
import os
import pytest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../api/controller'))
sys.path.append(parent_dir)

# pylint: disable=wrong-import-position, redefined-outer-name
from financestub import app as my_app

@pytest.fixture()
def app():
    '''declare  app'''
    app = my_app
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    '''return test client'''
    return app.test_client()


@pytest.fixture()
def runner(app):
    '''return test runner'''
    return app.test_cli_runner()
