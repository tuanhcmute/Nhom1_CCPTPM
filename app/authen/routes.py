from flask import render_template, request, make_response, redirect, url_for,session
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
  role_user = request.form.get("user")
  role_admin = request.form.get("admin")
  if(role_admin is not None):
    role = int(role_admin)
  elif (role_user is not None):
    role = int(role_user)
  try:
    user = User.query.filter_by(username=username).first()
    userDb = User.query.filter_by(username=username,roleId=role).first()
    if (user is not None) and (userDb is None):
      error = 'Access Denied'
      session['message'] = error
      return redirect(request.referrer)
    if userDb and password == userDb.password:
        user = User(username, role, password)
        print(user)
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
        error = 'Invalid username or password'
        session['message'] = error
        return redirect(request.referrer)
  except Exception as e:
      print('An error occurred while querying the database:', str(e))
      error = 'An error occurred while querying the database'
      session['message'] = error
      return redirect(request.referrer)


@bp.route('/logout', methods=[Method.GET])
@login_required
def logout():
  response = make_response(redirect('/auth/login'))
  response.delete_cookie('access_token')
  response.delete_cookie('username')
  logout_user()
  session.pop('message', None)
  return response

