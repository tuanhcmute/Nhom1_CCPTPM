from flask_login import UserMixin
from app.extensions import db
from app.model.role import Role

class User(db.Model, UserMixin):
  __tablename__ = 'tblUser'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  avatar = db.Column(db.String, nullable=True)
  age = db.Column(db.Integer, nullable=True)
  fullname = db.Column(db.String, nullable=True)
  address = db.Column(db.String, nullable=True)
  isEnable = db.Column(db.Boolean, nullable=True)
  roleId = db.Column(db.Integer, db.ForeignKey(Role.id))


  def __init__(self,roleId, username, password, email = None,avatar = None, age=None, fullname=None, address=None, isEnable=None):
    self.username = username
    self.password = password
    self.email = email
    self.avatar = avatar
    self.age = age
    self.fullname = fullname
    self.address = address
    self.isEnable = isEnable
    self.roleId = roleId
  
  def __repr__(self):
    return f'<User "{self.username}">'

  def __getattribute__(self, __name):
    return super().__getattribute__(__name)

  def to_dict(self):
      return {
        "username": self.username,
        "email": self.email,
        "avatar": self.avatar,
        "age": self.age,
        "address": self.address,
        "fullname": self.fullname,
        "role": self.Role.roleName
      }
