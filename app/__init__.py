from flask import Flask
from flask_login import LoginManager

from app.config import Config
from app.extensions import db, database_is_empty
from app.model import * 


def createApp():

  app = Flask(__name__)

  # Using login manager
  loginManager = LoginManager()
  loginManager.init_app(app=app)
  loginManager.login_view = 'authen.index'
  @loginManager.user_loader
  def loadUser(id):
      return User.query.get(int(id))

  # Config app
  defaultConfig = Config()
  app.config.from_object(defaultConfig)
  
  # Initialize Flask extensions here if code block using testcases
  if app.config['SQLALCHEMY_DATABASE_URI'] is None:
    # Do not change code below => If you change, can not merge code
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ubuntu:1@localhost:5432/apiDashboard"
  db.init_app(app)
  
  # Create table if have no table in database
  if(database_is_empty(app.config['SQLALCHEMY_DATABASE_URI'])):
    with app.app_context():
      db.create_all()
      init_record()

  return app


def init_record():
  # Create role
  userRole = Role('user')
  adminRole = Role('admin')
  db.session.add_all([userRole, adminRole])
  db.session.commit()

  # Create admin account
  adminRoleDB = Role.query.filter_by(roleName='admin').first()
  adminUser = User(roleId=adminRoleDB.id,username='admin', password='admin', age=18,fullname='admin', address='Hanoi', isEnable=True)
  db.session.add_all([adminUser])
  db.session.commit()