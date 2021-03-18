from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///tsoha"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registerform")
def registerform():
    return render_template("registerform.html")

@app.route("/registerresult", methods=["POST"])
def registerresult():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT username from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user != None:
        return "User name already taken"
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":password})
    db.session.commit()
    session["username"] = username
    return redirect("/")

@app.route("/loginform")
def loginform():
    return render_template("loginform.html")

@app.route("/loginresult", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return "No user with that name"
    elif user["password"] != password:
        return "Wrong password"
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")