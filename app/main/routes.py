from flask import render_template, make_response, request
from flask_login import  login_required

from app.main import bp
from app.utils.contants import Method
from app.vendor.getToken import getToken
from app.vendor.getData import getData

@bp.after_request
@login_required
def refreshToken(response):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            tokenDic = getToken()
            accessToken, maxAge = tokenDic['access_token'], tokenDic['expires_in']
            response.set_cookie('access_token', accessToken, max_age=maxAge)
        return response
    except (RuntimeError, KeyError):
        return response

@bp.route('/', methods=[Method.GET])
@login_required
def index():
    username = request.cookies.get('username')
    return render_template('index.html', username=username)

@bp.route('/data', methods=[Method.GET])
@login_required
def getSampleData():
    # Get token
    token = request.cookies.get('access_token')
    data = getData(token)
    print(len(data))
    return data
