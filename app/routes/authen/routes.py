from flask import render_template, request, make_response, redirect, url_for,session, Flask
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

import re
import os
from app.routes.authen import bp
from app.utils.contants import Method
from app.model.user import User
from app.utils.contants import URI
from app.vendor.getToken import getToken
from app.extensions import db
import random
import smtplib
import pyotp
import time

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


    if userDb.isEnable == False: 
      error = 'Invalid username or password'
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
        response.set_cookie('role', str(role))
        return response
    else:
        error = 'Invalid username or password'
        session['message'] = error
        return redirect(request.referrer)
  except Exception as e:
      print('An error occurred while querying the database:', str(e))
      error = str(e)
      session['message'] = error
      return redirect(request.referrer)


#----------------------LOGOUT----------------------#

@bp.route('/logout', methods=[Method.GET])
@login_required
def logout():
  response = make_response(redirect('/auth/login'))
  response.delete_cookie('access_token')
  response.delete_cookie('username')
  response.delete_cookie('role')
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
      email = request.form.get('email')
      avatar = request.form.get('avatar')
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
      user = User(role, username, hashed_password,email,avatar, age, fullname, address, isEnable=True)
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
  try:
      #get_data
      email = request.form.get('email')

      # Check email exists
      if check_email() != 'Success':
        error = 'Email của bạn không đúng. Vui lòng nhập chính xác Email'
        session['message_forgot_password'] = error
        return redirect(request.referrer)
      
      # Save Pass
      ###Sent OTP
      # Create Secret Key
      secret_key = pyotp.random_base32()

      # Generate OTP
      totp = pyotp.TOTP(secret_key, interval=300)
      OTP = totp.now()
      print("OTP: "+ OTP)

      # Get expiration time of an OTP code
      expires_at = time.time() + totp.interval
      exp_time = time.strftime('%H:%M:%S %d/%m/%Y', time.localtime(expires_at))
      print(exp_time)
      

      ## Send OTP via email
      # Get email account from .env
      sent_mail_user = os.getenv('MAIL_USERNAME')
      sent_mail_pass = os.getenv('MAIL_PASSWORD')

      sender_email = sent_mail_user
      sender_password = sent_mail_pass
      receiver_email = email
      message = f'Subject: Password Reset\n\nWe have received a request to reset the password for your account. \nYour OTP is: {OTP}. \nPlease enter this code on the password reset page to proceed. This code will be valid until {exp_time}.\n\nIf you did not request a password reset, please ignore this message and take appropriate measures to secure your account.\n\nThank you for using our service.\n\nBest regards,\nGroup 01'
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(sender_email, sender_password)
      server.sendmail(sender_email, receiver_email, message)
      server.quit()
      

      # Clear Session
      session.pop('message_forgot_password', None)


      response = make_response(redirect(url_for('authen.getResetPasswordForm', check = True)))
      # Set cookie
      response.set_cookie('secret_key', secret_key, max_age=300, httponly=True, secure=True)
      response.set_cookie('email', email, max_age=300, httponly=True, secure=True)
      return response
  except Exception as e:
      print('An error occurred while querying the database:', str(e))
      error = 'Error'
      session['message_forgot_password'] = error
      return redirect(request.referrer)

#--------------------Reset Password----------------#
@bp.route('/reset-password', methods=[Method.GET])
def getResetPasswordForm():
  check = request.args.get('check')
  if check:
    return render_template('resetpassword.html', check_sentOTP = 'True')
  return render_template('resetpassword.html')

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    #Get Data
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    user_otp = str(request.form.get('OTP'))

    #Check new_password and confirm_password
    if(new_password != confirm_password):
      error = 'Mật khẩu không khớp'
      session['message_reset_password'] = error
      return redirect(request.referrer)

    #Check Strong Password 
    check_pass= check_password(new_password)
    if(check_pass != 'Success'):
      error = check_pass
      session['message_reset_password'] = error
      return redirect(request.referrer)
    
    # Get secret_key and email form cookies
    secret_key = request.cookies.get('secret_key')
    email = request.cookies.get('email')

    if not secret_key:
      error = f'Bạn Không Thể Xác Thực OTP. Vui lòng quay lại trang Forgot Password'
      session['message_reset_password'] = error
      return redirect(request.referrer)
    # Create TOTP
    totp = pyotp.TOTP(secret_key, interval=300)

    # Create check Verify
    check = False
    try:
      # Verify
      if totp.verify(user_otp):
        user = User.query.filter_by(email = email).first()
        if user:
            #Hash Password
            app = Flask(__name__)
            csrf = CSRFProtect(app)
            BcryptPass = Bcrypt(app)
            hashed_password = BcryptPass.generate_password_hash(new_password).decode('utf-8')

            #Save 
            user.password = hashed_password
            db.session.commit()
            check = True
      else:
        error = f'OTP không chính xác. Vui lòng thử lại!!'
        session['message_reset_password'] = error
        return redirect(request.referrer)
          
      # Create Response
      response = make_response(render_template('resetpassword.html', check=check))
      if check:
        response.delete_cookie('secret_key')
        response.delete_cookie('email')
      return response   
    except:
        print("Mã OTP không hợp lệ, xác thực thất bại")
    
      
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
  email = request.form.get('email')

  # Kiểm tra username có tồn tại hay không
  user = User.query.filter_by(username=username).first()
  email = User.query.filter_by(email=email).first()
  if user is not None:
    return 'Username đã tồn tại'
  if email is not None:
    return 'Email đã được sử dụng'
  
  return 'Success'

def check_data_login():
  # Lấy giá trị từ các trường của form
  role_user = request.form.get("user")
  role_admin = request.form.get("admin")
  role = 0
  if(role_admin is not None):
    role = int(role_admin)
  elif (role_user is not None):
    role = int(role_user)
  # Kiểm tra xem các trường này có được điền đầy đủ hay không
  if role == 0:
    return 'Vui lòng click vào checkbox Role'
  
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

#------------- Check Email --------------#
def check_email():
  try:
    email = request.form.get('email')
    user = db.session.query(User).filter(User.email==email).first()
    if user:
      return 'Success'
    else:
      return 'The email does not exist.'
  except Exception as e:
    print("NOT OK")