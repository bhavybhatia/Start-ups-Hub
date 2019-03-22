from flask import Flask,render_template,redirect,url_for,request,session
import os
import pyrebase
import firebase_admin
from firebase_admin import credentials,auth

app=Flask(__name__)
app.secret_key = os.urandom(12)

cred = credentials.Certificate("")  #Your Firebase Credential json file in the quotes...
firebase_admin.initialize_app(cred)
#------------------------------------------------ Maintaining Configurations ---------------------------------------------------

#------------------------------------------------ Object Building Section ---------------------------------------------------
firebase = pyrebase.initialize_app(config)
auth1=firebase.auth()
database=firebase.database()
#------------------------------------------------ Maintaining Create User Section ---------------------------------------------------
@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        name=request.form['name']
        phone=request.form['contact']
        try:
            error2="Seems like Email id already Exist."
            user=auth1.create_user_with_email_and_password(email,password)
            # auth1.send_email_verification(user['idToken'])
            uid=user['localId']
            data={"name":name,"phone":phone,"status":"1"}
            database.child("users").child(uid).child("details").set(data)
        except:
            return render_template("home.html",error2=error2)

        return redirect(url_for('login'))
    else:
        return render_template("home.html")
#------------------------------------------------ Maintaining Login Section ---------------------------------------------------
@app.route('/login',methods=['POST','GET'])
def login():
    session.pop('user',None)
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            error="Invalid Credentials"
            user=auth1.sign_in_with_email_and_password(email,password)
            session['user']=email
        except:
            return render_template("login.html",error=error)

        return redirect(url_for('signedin'))

    else:
        return render_template("login.html")
#------------------------------------------------ Maintaining Password-Reset Section ---------------------------------------------------
@app.route('/reset',methods=['POST','GET'])
def reset():
    if request.method=='POST':
        email1=request.form['email']
        try:
            error1="This email id is not registered with us"
            auth1.send_password_reset_email(email1)
        except:
            return render_template("reset.html",error1=error1)
        return redirect(url_for('login'))
    else:
        return render_template("reset.html")
#------------------------------------------------ Maintaining Home/Post-Login Section ---------------------------------------------------
@app.route('/signedin')
def signedin():
    if 'user' in session:
        username=session['user']
        return render_template("signin.html",username=username)
    else:
        return render_template("Auth_failed.html")



#------------------------------------------------ Maintaining StartUp-Adding Section ---------------------------------------------------
@app.route('/startupAdd')
def startupAdd():
    return render_template("startupAdd.html")

#------------------------------------------------ Maintaining Host/Run Section (Do not Interrupt) ---------------------------------------------------
if __name__=="__main__":
    app.run()
