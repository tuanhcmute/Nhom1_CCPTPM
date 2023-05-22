import pytest
from tests import app

@pytest.fixture(scope='function')
def client(app):
  return app.test_client()


    