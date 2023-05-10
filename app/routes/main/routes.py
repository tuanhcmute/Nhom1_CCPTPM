from flask import render_template, request, jsonify, make_response
from flask_login import  login_required

from app.routes.main import bp
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
    try:
        # Get token
        token = request.cookies.get('access_token')
        # # Get data
        data = getData(token, 12, 2022)
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
    except Exception as e:
        print(str(e))
        return str(e)


@bp.route('/charts', methods=[Method.GET])
@login_required
def getChartsPage():
    return render_template('charts.html')

@bp.route('/tables', methods=[Method.GET])
@login_required
def getTablesPage():
    return render_template('tables.html')

@bp.route('/profile', methods=[Method.GET])
@login_required
def getProfile():
    return render_template('profile.html')

@bp.route('/data', methods=[Method.GET])
@login_required
def getSampleData():
    
    # Get data
    month = request.args.get('month')
    year = request.args.get('year')
    # Check data
    if type(month) == str:
        month = int(month)
    if type(year) == str:
        year = str(year)

    # Get token
    token = request.cookies.get('access_token')
    # Get data
    data = getData(token, month=month, year=year)
    if data is None:
        return 'error'
    return data