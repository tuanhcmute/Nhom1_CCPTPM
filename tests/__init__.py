import pytest
from app import createApp, init_record
from app.extensions import db
import os

@pytest.fixture(scope='session')
def app():
  os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
  app = createApp()
  app.config.update({'TESTING': True,'SECRET_KEY':'your_secret_key'})
  ctx = app.app_context()
  if db is not None:
    with ctx:
      db.drop_all()
      ctx.push()
  with ctx:
    db.create_all()
    init_record()
    ctx.push()
  yield app
