from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __init__(self, username, password):
    self.username = username
    self.password = password
