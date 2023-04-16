from flask import Blueprint

bp = Blueprint('usermanage', __name__)

from app.routes.admin.usermanage import routes