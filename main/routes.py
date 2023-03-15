from flask import render_template
from flask_login import  login_required

from main import bp
from utils.contants import Method

@bp.route('/', methods=[Method.GET])
@login_required
def index():
    return render_template('index.html')