from flask import Blueprint

bp = Blueprint('main', __name__)

from main import routes