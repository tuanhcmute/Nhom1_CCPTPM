import pytest
from app import createApp
from app.extensions import db
import os

@pytest.fixture
def app():
  os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
  app = createApp()
  app.config.update({'TESTING': True,'SECRET_KEY':'your_secret_key'})
  ctx = app.app_context()
  with ctx:
    db.create_all()
  ctx.push()
  yield app
  with ctx:
    db.drop_all


