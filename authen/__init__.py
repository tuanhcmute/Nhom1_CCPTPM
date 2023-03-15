from flask import Blueprint

bp = Blueprint('authen', __name__)

from authen import routes