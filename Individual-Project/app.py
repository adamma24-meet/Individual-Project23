from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
firebaseConfig = {
  "apiKey": "AIzaSyDEJTccnPD3ZDDATrdNyEYa3uR8Rxhjz4M",
  "authDomain": "individual-38786.firebaseapp.com",
  "databaseURL": "https://individual-38786-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "individual-38786",
  "storageBucket": "individual-38786.appspot.com",
  "messagingSenderId": "483272818954",
  "appId": "1:483272818954:web:9cdb826c7fb0f6cf22faf3",
  "measurementId": "G-JZJ7XL28DD"
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


#Code goes below here
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {'email':email, 'username':username, 'score': 0}
            uid = login_session['user']['localId']
            db.child('users').child(uid).set(user)
            return redirect(url_for('index'))
        except:
           error = "Authentication failed"

    return render_template("signup.html")
@app.route('/main',methods=['GET','POST'])
def main():
    return render_template("main.html")
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            print(login_session['user'], "heyyYYYYYYYYYYYYYYYYYYYYYY")
            return render_template("index.html")
        except Exception as e:
            print('ERROR:', e)
            error = "Authentication failed"
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        score = request.form['score']
        UID = login_session['user']['localId']
        print(UID)
        print(db.child('users').child(UID).get().val())
        email = db.child('users').child(UID).get().val()['email']
        username = db.child('users').child(UID).get().val()['username']
        leaderboardScore = {"email":email, "username":username, 'score':score}
        db.child('users').child(UID).update(leaderboardScore)
        print(score)
    return render_template('index.html')

@app.route('/leaderboard', methods=["POST", "GET"])
def leaderboard():
    UID = login_session['user']['localId']
    score = db.child('users').child(UID).get().val()['score']
    return render_template('highscore.html', score = score)

#Code goes above here
users = db.child("Users").get().val()
print(users)
if __name__ == '__main__':
    app.run(debug=True)