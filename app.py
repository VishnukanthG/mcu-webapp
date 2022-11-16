from random import randint, random
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "abc" 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mcu.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class mcu(db.Model):
    userid = db.Column(db.Integer, primary_key = True, unique = True)
    username = db.Column(db.String(20), nullable = False, primary_key = True)
    password = db.Column(db.String(20), nullable = False)

# class RegisterForm(FlaskForm):
#     username = StringField{validator=[InputRequired(), Length(min=4, max=20)], render_kw = {"placeholder" : "Username"}}
@app.route("/")
def landingpage():
    return render_template("index.html")



@app.route("/login", methods = ['GET','POST'])
def login():

    if request.method == "POST":
        loginuserid = request.form['loginuserid']
        loginusername = request.form['loginusername']
        loginpassword = request.form['loginpassword']

        if loginuserid == "" and loginusername == "" and loginpassword == "" :
            flash("Please fill the details")
            return render_template('login.html')

        useri = mcu.query.filter_by( userid = int(loginuserid), username = loginusername, password = loginpassword).first()

        if useri :
            return render_template('homepage.html', loginuserid = loginuserid, loginusername = loginusername)

        else:
            flash("Login credentials are incorrect")
            return redirect("/login")    
       
    return render_template('login.html')
    
@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']    

        if username == "" and password == "":
            flash("Please fill the details")
            return render_template("signup.html")


        user1 = mcu.query.filter_by( username = username ).first()
        if  user1 :
            flash("User already exist")
            return redirect("/signup")

        else:
            uid = mcu(userid = randint(12405,20000), username = username, password = password)
            db.session.add(uid)
            db.session.commit()
            return render_template("ak.html", userid = uid.userid)

    return  render_template("signup.html")

@app.route("/homepage")
def homepage():
    return render_template('homepage.html')

@app.route("/ak")
def ak():
    return render_template('ak.html')

if __name__ == "__main__" :
    app.run(debug=True, port = 8000)
