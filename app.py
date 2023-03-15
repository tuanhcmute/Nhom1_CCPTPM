from flask import Flask, request
from flask_login import LoginManager

from config import Config
from extensions import db
from model.user import User
from vendor.getToken import getToken

app = Flask(__name__)

# Using login manager
loginManager = LoginManager()
loginManager.init_app(app=app)
loginManager.login_view = 'authen.index'
@loginManager.user_loader
def loadUser(id):
    return User.query.get(int(id))

# Config app
app.config.from_object(Config)
# Initialize Flask extensions here
db.init_app(app)


# Register blueprints
from main import bp as mainBp
app.register_blueprint(mainBp)
from authen import bp as authenBp
app.register_blueprint(authenBp, url_prefix='/auth')