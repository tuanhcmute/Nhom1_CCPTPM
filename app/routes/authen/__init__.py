from flask import Blueprint

bp = Blueprint('authen', __name__)

from app.routes.authen import routes