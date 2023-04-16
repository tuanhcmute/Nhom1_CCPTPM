from flask import render_template, make_response, request, json, jsonify
from flask_login import  login_required

from app.routes.admin.usermanage import bp
from app.utils.contants import Method
from app.vendor.getToken import getToken
from app.vendor.getData import getData
from app.extensions import cache, db
from app.model import *


@bp.route('/', methods=[Method.GET])
@login_required
def getListUser():
    is_enable = True
    users = User.query.filter_by(isEnable=is_enable).all()
    return render_template('user-manage/list-user.html', users=users)

@bp.route('/delete', methods=[Method.DELETE])
@login_required
def deleteUser():
    try:
        dict_keys = request.form
        user_id = dict_keys['userId']
        user = User.query.filter_by(id=user_id).first()
        # Update user
        user.isEnable = False
        db.session.commit()
        return jsonify({"message": "Delete user success", "status": "OK"})
    except Exception as e:
        return jsonify({"message": str(e), "status": "ERROR"})

@bp.route('/find-by-id', methods=[Method.GET])
@login_required
def getUserByUserId():
    user_id =  request.args.get('userId')
    user = User.query.filter_by(id=user_id).first()
    return json.dumps(user.to_dict())


@bp.route('/update', methods=[Method.POST])
@login_required
def udpateUser():
    try:
        user_id = request.form['userId']
        address = request.form['address']
        fullname = request.form['fullname']
        age = int(request.form['age'])
        avatar = request.form['avatar']
        userDB = User.query.filter_by(id=user_id).first()
        if userDB:
            userDB.age = age
            userDB.fullname = fullname
            userDB.address = address
            userDB.avatar = avatar
            db.session.commit()
        return jsonify({"message": "Update user success", "status": "OK"})
    except Exception as e:
        return jsonify({"message": str(e), "status": "ERROR"})

@bp.route('/trash', methods=[Method.GET])
@login_required
def getListUserDeleted():
    is_enable = False
    users = User.query.filter_by(isEnable=is_enable).all()
    return render_template('user-manage/list-user-deleted.html', users=users)

@bp.route('/recovery', methods=[Method.GET])
@login_required
def recoveryUserDeleted():
    try:
        is_enable = False
        users = User.query.filter_by(isEnable=is_enable).all()
        for user in users:
            user.isEnable = True
        db.session.commit() 
        return jsonify({'message': 'Recovery success', 'status': 'OK'})
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'ERROR'})

@bp.route('/delete-all', methods=[Method.GET])
@login_required
def deleteAllUserDeleted():
    try:
        is_enable = False
        users = User.query.filter_by(isEnable=is_enable).all()
        if users:
            for user in users:
                db.session.delete(user)
            db.session.commit()
        return jsonify(
            {
            'message': "Empty trash success",
            'status': 'OK'
            }
        )
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'ERROR'})


