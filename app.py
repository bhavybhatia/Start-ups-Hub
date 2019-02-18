from flask import Flask,render_template,redirect,url_for,request
import pyrebase

app=Flask(__name__)

config={
    "apiKey": "AIzaSyDKv6XkAjA3y8IQ_iaM9CEFArxpnjpidvk",
    "authDomain": "start-ups-hub.firebaseapp.com",
    "databaseURL": "https://start-ups-hub.firebaseio.com",
    "projectId": "start-ups-hub",
    "storageBucket": "start-ups-hub.appspot.com",
    "messagingSenderId": "575334323699"
}

firebase = pyrebase.initialize_app(config)
auth=firebase.auth()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signin',methods=['POST','GET'])

def signin():
    check="Please Check Your Credientials"
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            user=auth.sign_in_with_email_and_password(email,password)
        except:
            return redirect(url_for('login'))

        return render_template("signin.html")

    else:
        return redirect(url_for('login'))

@app.route('/success',methods=['POST','GET'])
def success():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=auth.create_user_with_email_and_password(email,password)
        auth.send_email_verification(user['idToken'])
        return render_template("success.html",email=email)

    else:
        return redirect(url_for('home'))

@app.route('/reset')
def reset():
    return render_template("reset.html")

@app.route('/resetDone',methods=['POST','GET'])
def resetDone():
    if request.method=='POST':
        email1=request.form['email']
        auth.send_password_reset_email(email1)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

if __name__=="__main__":
    app.run()
