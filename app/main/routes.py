from flask import render_template, make_response, request, jsonify
from flask_login import  login_required
from datetime import datetime

from app.main import bp
from app.utils.contants import Method
from app.vendor.getToken import getToken
from app.vendor.getData import getData
from app.extensions import cache, db
from app.model import *

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

    # Get token
    token = request.cookies.get('access_token')
    # Get data
    data = getData(token)

    totalHO = 0
    totalItemInHo = 0
    totalStatusOK = 0
    totalStatusFail = 0

    totalHO = len(data)
    for keyHO in data:
        childrenDict = data.get(keyHO)
        totalItemInHo = totalItemInHo + len(childrenDict)
        for hashKey in childrenDict:
            itemDict = childrenDict[hashKey]
            if itemDict['status'] == 'ok':
                totalStatusOK = totalStatusOK + 1
            else: 
                totalStatusFail = totalStatusFail + 1

    username = request.cookies.get('username')
    return render_template('index.html', 
                           username=username, 
                           totalHO=totalHO, 
                           totalItemInHo=totalItemInHo, 
                           totalStatusOK=totalStatusOK, 
                           totalStatusFail=totalStatusFail, data=data)


@bp.route('/profile', methods=[Method.GET])
@login_required
def getProfile():
    return render_template('profile.html')

@bp.route('/admin/user-manage', methods=[Method.GET])
@login_required
def getListUser():
    is_enable = True
    users = User.query.filter_by(isEnable=is_enable).all()
    return render_template('user-manage/list-user.html', users=users)

@bp.route('/admin/user-manage/delete', methods=[Method.DELETE])
@login_required
def deleteUser():
    dict_keys = request.form
    user_id = dict_keys['userId']
    user = User.query.filter_by(id=user_id).first()
    # Update user
    user.isEnable = False
    db.session.commit()
    return 'hello world'


@bp.route('/data', methods=[Method.GET])
@login_required
def getSampleData():
    # Get token
    token = request.cookies.get('access_token')
    # Get data
    data = getData(token)
    return data