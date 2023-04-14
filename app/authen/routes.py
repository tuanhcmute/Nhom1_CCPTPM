from flask import render_template, request, make_response, redirect, url_for,session, Flask
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

import re
from app.authen import bp
from app.utils.contants import Method
from app.model.user import User
from app.utils.contants import URI
from app.vendor.getToken import getToken
from app.extensions import db

@bp.route('/login', methods=[Method.GET])
def index():
  response = make_response()
  response.data = 'hello world'
  return render_template('login.html')


@bp.route('/login', methods=[Method.POST])
def loginPost():
  check_data = check_data_login()
  if check_data != 'Success':
    error = check_data
    session['message'] = error
    return redirect(request.referrer)
  try:
    #Get Data
    username = request.form.get('username')
    password = request.form.get('password')
    role_user = request.form.get("user")
    role_admin = request.form.get("admin")
    if(role_admin is not None):
      role = int(role_admin)
    elif (role_user is not None):
      role = int(role_user)
    
    #Query data
    user = User.query.filter_by(username=username).first()
    userDb = User.query.filter_by(username=username,roleId=role).first()

    #Check role when username and password is correct
    if (user is not None) and (userDb is None):
      error = 'Access Denied'
      session['message'] = error
      return redirect(request.referrer)
    
    # Create Bcrypt for Check Pass
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    bcrypt = Bcrypt(app)

    if userDb and bcrypt.check_password_hash(userDb.password, password):
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

@bp.route('/signup', methods=[Method.GET])
def getSignUpForm():
  return render_template('signup.html')

@bp.route('/signup', methods=[Method.POST])
def SignUp():
  message_signup = check_user_data_signup()
  if (message_signup != 'Success'):
    error = message_signup
    session['message_signup'] = error
    return redirect(request.referrer)
  
  try:
      #get_data
      username = request.form.get('username')
      password = request.form.get('password')
      fullname = request.form.get('fullname')
      address = request.form.get('address')
      age = request.form.get('age')
      role = int(request.form.get('user_type'))

      #Check Strong password
      check_pass= check_password(password)
      if(check_pass != 'Success'):
        error = check_pass
        session['message_signup'] = error
        return redirect(request.referrer)
      
      #hash Password
      app = Flask(__name__)
      csrf = CSRFProtect(app)
      BcryptPass = Bcrypt(app)
      hashed_password = BcryptPass.generate_password_hash(password).decode('utf-8')
      
      #create user
      user = User(role, username, hashed_password, age, fullname, address, isEnable=True)
      db.session.add_all([user])
      db.session.commit()

      session.pop('message_signup', None)
      
      return render_template('signup.html', check='true')
  except Exception as e:
      print('An error occurred while querying the database:', str(e))
      error = 'Error'
      session['message_signup'] = error
      return redirect(request.referrer)


# Clear session
@bp.route('/form_login')
def clear_session_login():
  if 'message_signup' in session:
    session.pop('message_signup', None)
  return redirect(url_for('authen.loginPost'))

@bp.route('/form_signup')
def clear_session_signup():
  if 'message' in session:
    session.pop('message', None)
  return redirect(url_for('authen.SignUp'))

@bp.route('/clear_session')
def clear_session():
  session.clear()
  return 'Session cleared'



# Check Data
def check_user_data_signup():
  # Lấy giá trị từ các trường của form
  username = request.form.get('username')
  password = request.form.get('password')
  fullname = request.form.get('fullname')
  address = request.form.get('address')
  age = request.form.get('age')
  # Kiểm tra xem các trường này có được điền đầy đủ hay không
  if not username:
      return 'Vui lòng nhập tên đăng nhập'
  if not password:
      return 'Vui lòng nhập mật khẩu'
  if not fullname:
      return 'Vui lòng nhập tên'
  if not age:
      return 'Vui lòng nhập tuổi'
  if not address:
      return 'Vui lòng nhập địa chỉ'
  
  # Kiểm tra username có tồn tại hay không
  user = User.query.filter_by(username=username).first()
  if user is not None:
    return 'Username đã tồn tại'
  
  return 'Success'

def check_data_login():
  # Lấy giá trị từ các trường của form
  username = request.form.get('username')
  password = request.form.get('password')
  role_user = request.form.get("user")
  role_admin = request.form.get("admin")
  role = 0
  if(role_admin is not None):
    role = int(role_admin)
  elif (role_user is not None):
    role = int(role_user)
  # Kiểm tra xem các trường này có được điền đầy đủ hay không
  if not username:
    return 'Vui lòng nhập tên đăng nhập'
  if not password:
    return 'Vui lòng nhập mật khẩu'
  if role == 0:
    return 'Vui lòng click vào checkbox Role'
  
  return 'Success'

# Check Strong pass
def check_password(password):
    # Kiểm tra độ dài mật khẩu
    if len(password) < 6 or len(password) > 20:
      return 'Mật khẩu phải từ 6 đến 20 ký tự'

    # Kiểm tra các ký tự trong mật khẩu
    if not re.search(r'\d', password):
      return'Mật khẩu phải chứa ít nhất một số'
    if not re.search(r'[A-Z]', password):
      return 'Mật khẩu phải chứa ít nhất một chữ hoa'
    if not re.search(r'[a-z]', password):
      return 'Mật khẩu phải chứa ít nhất một chữ thường'

    # Nếu mật khẩu thỏa mãn tất cả các yêu cầu
    return 'Success'
