import pytest
from tests import app

@pytest.fixture()
def client(app):
  return app.test_client()
    