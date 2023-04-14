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
import random
import smtplib
import pyotp


#------------------LOGIN--------------------#

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


#----------------------LOGOUT----------------------#

@bp.route('/logout', methods=[Method.GET])
@login_required
def logout():
  response = make_response(redirect('/auth/login'))
  response.delete_cookie('access_token')
  response.delete_cookie('username')
  logout_user()
  session.pop('message', None)
  return response



#-------------------SIGNUP------------------#

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


#-----------------Forgot Password-----------------#

@bp.route('/forgot-password', methods=[Method.GET])
def getForgotPasswordForm():
  return render_template('forgotpassword.html')

@bp.route('/forgot-password', methods=[Method.POST])
def ForgotPassword():
  message_forgot_password = check_data_forgot_password()
  if ( message_forgot_password != 'Success'):
    error =  message_forgot_password
    session['message_forgot_password'] = error
    return redirect(request.referrer)
  try:
      #get_data
      email = request.form.get('email')
      new_password = request.form['new_password']
      confirm_password = request.form['confirm_password']

      #Check new_password and confirm_password
      if(new_password != confirm_password):
        error = 'Mật khẩu không khớp'
        session['message_forgot_password'] = error
        return redirect(request.referrer)

      #Check Strong Password 
      check_pass= check_password(new_password)
      if(check_pass != 'Success'):
        error = check_pass
        session['message_forgot_password'] = error
        return redirect(request.referrer)
      

      ###Sent OTP
      # Generate OTP
      totp = pyotp.TOTP(pyotp.random_base32())
      OTP = totp.now()

      # Create Secret Key
      secret_key = pyotp.random_base32()
      session['secret_key'] = secret_key

      # Send OTP via email
      sender_email = 'zzro333@gmail.com'
      sender_password = 'wiibdoxuisaydfnb'
      receiver_email = email
      message = f'Subject: Password Reset OTP\n\nYour OTP is {otp}.'
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(sender_email, sender_password)
      server.sendmail(sender_email, receiver_email, message)
      server.quit()
      
      #return render_template('reset_password.html', email=email)

      # Clear Session
      session.pop('message_forgot_password', None)

      return render_template('resetpassword.html', email = email)
  except Exception as e:
      print('An error occurred while querying the database:', str(e))
      error = 'Error'
      session['message_signup'] = error
      return redirect(request.referrer)

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    user_otp = request.form['otp']
    new_password = request.form['new_password']
    
    # Verify OTP
    if int(user_otp) == otp:
        # Update password in database
        # ...
        return 'Password reset successful!'
    else:
        return 'Invalid OTP.'
#-----------------Clear session-----------------#
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



#-------------------Check Data------------------#
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

def check_data_forgot_password():
    email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    if not email:
      return 'Vui lòng điền Email'
    elif not new_password:
      return 'Vui lòng điền mật khẩu mới' 
    elif not confirm_password:
      return 'Vui lòng xác nhận mật khẩu mới'
    return 'Success'

#--------------Check Strong Pass------------------#
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

