from admin import app,db
from flask import request, session
import flask_admin
from flask_login import login_user
from bson import json_util, ObjectId
import json
from werkzeug.security import generate_password_hash, check_password_hash
from admin.model.mysql import User
import datetime

def checkloginusername():
    email = request.form["email"]
    print(email)
    user = db.session.query(User).filter_by(login=email).first()
    if user is None:
        return "No User"
    else:
        return "User exists"

def checkloginpassword():
    email = request.form["email"]
    user = db.session.query(User).filter_by(login=email).first()
    password = request.form["password"]
    hashpassword = check_password_hash(password)
    print(user.email,user.password)
    if check_password_hash(user.password,password) :
        login_user(user,remember=True, duration=datetime.timedelta(days=30))
        return "correct"
    else:
        return "wrong"
    
def checkemail():
    email = request.form["email"]
    check = db.session.query(User).filter_by(login=email).first()
    if check is None:
        return "Available"
    else:
        return "This Email Already Exist"

def registerUser():
    user = User()
    fields = [k for k in request.form]               
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = generate_password_hash(user_data["password"])
    user_data["confirmpassword"] = generate_password_hash(user_data["confirmpassword"])

    user.auth = u'Regular'
    user.email = user_data['email']
    user.nickname = user_data['nickname']
    user.password = user_data['password']

    db.session.add(user)
    db.session.commit()
    print("[Notice]User Resister Done")