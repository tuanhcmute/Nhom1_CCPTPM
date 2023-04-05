from flask import render_template, request, make_response, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app.authen import bp
from app.utils.contants import Method
from app.model.user import User
from app.utils.contants import URI
from app.vendor.getToken import getToken


@bp.route('/login', methods=[Method.GET])
def index():
  response = make_response()
  response.data = 'hello world'
  return render_template('login.html')


@bp.route('/login', methods=[Method.POST])
def loginPost():
  username = request.form.get('username')
  password = request.form.get('password')
  userDb = User.query.filter_by(username=username).first()
  if userDb and password == userDb.password:
    user = User( username, password)
    user.id = userDb.id
    login_user(user)

    response = make_response(redirect(URI.HOME))
    tokenDic = getToken()
    accessToken, maxAge = tokenDic['access_token'], tokenDic['expires_in']
    # Set cookie
    response.set_cookie('access_token', accessToken, max_age=maxAge)
    response.set_cookie('username', username)
    return response
  else:
    return 'Invalid username or password'


@bp.route('/signup', methods=[Method.GET])
def getSignUpForm():
  return render_template('signup.html')


@bp.route('/logout', methods=[Method.GET])
@login_required
def logout():
  response = make_response(redirect('/auth/login'))
  response.delete_cookie('access_token')
  response.delete_cookie('username')
  logout_user()
  return response

