from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from app.config import Config
from app.extensions import db, database_is_empty, cache
from app.model import * 

def createApp():

  app = Flask(__name__)
  CORS(app=app)
  # CORS(app)
  app.config['CACHE-TYPE'] = 'SimpleCache'
  cache.init_app(app)

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
  # Hash password
  app = Flask(__name__)
  csrf = CSRFProtect(app)
  BcryptPass = Bcrypt(app)
  hashed_password = BcryptPass.generate_password_hash('admin').decode('utf-8')
  
  #Create user
  adminUser = User(roleId=adminRoleDB.id,username='admin',email ='admin@gmail.com', avatar ='https://www.clipartmax.com/png/middle/319-3191274_male-avatar-admin-profile.png', password = hashed_password, age=18,fullname='admin', address='Hanoi', isEnable=True)
  db.session.add_all([adminUser])
  db.session.commit()