from flask_login import UserMixin
from app.extensions import db
from app.model.role import Role

class User(db.Model, UserMixin):
  __tablename__ = 'tblUser'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer, nullable=True)
  fullname = db.Column(db.String, nullable=True)
  address = db.Column(db.String, nullable=True)
  isEnable = db.Column(db.Boolean, nullable=True)
  roleId = db.Column(db.Integer, db.ForeignKey(Role.id))


  def __init__(self, username, password, age, fullname, address, isEnable, roleId):
    self.username = username
    self.password = password
    self.age = age
    self.fullname = fullname
    self.address = address
    self.isEnable = isEnable
    self.roleId = roleId

  def __repr__(self):
    return f'<User "{self.username}">'
