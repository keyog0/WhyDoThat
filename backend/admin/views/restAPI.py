from admin import app
from flask import send_from_directory
from flask import request, redirect, url_for, session
from admin.control import user_mgmt
from flask_login import logout_user,current_user

@app.route('/')
def index() :
    return send_from_directory('./build/', 'index.html')

@app.route('/register',methods=["GET","POST"])
def register() :
    if request.method == "GET" :
        return send_from_directory('./views/templates/','register.html')
    elif request.method == "POST" :
        user_mgmt.registerUser()
        return redirect(url_for('login'))

@app.route('/checkemail', methods=["POST"])
def check() :
    return user_mgmt.checkemail()

@app.route('/login',methods=["GET","POST"])
def login() :
    if request.method == "GET" :
        if not current_user.is_authenticated :
            return send_from_directory('./views/templates/','login.html')
        else :
            return redirect(url_for('index'))

@app.route('/checkloginemail', methods=["POST"])
def checkUserlogin():
    print('@'*20)
    return user_mgmt.checkloginemail()

@app.route('/checkloginpassword', methods=["POST"])
def checkUserpassword():
    return user_mgmt.checkloginpassword()

#The admin logout
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    logout_user()  # remove user session
    return redirect(url_for("login"))  # redirect to home page with message

#Forgot Password
@app.route('/forgot-password', methods=["GET"])
def forgotpassword():
    return render_template('forgot-password.html')

#404 Page
