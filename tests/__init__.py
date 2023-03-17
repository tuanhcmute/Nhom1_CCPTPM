import pytest
from app import createApp
from app.extensions import db

@pytest.fixture
def app():
  app = createApp()

  app.config.update({
    'TESTING': True,
  })
  with app.app_context():
    db.create_all()
 
  yield app

