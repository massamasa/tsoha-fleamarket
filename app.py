from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":password})
    db.session.commit()
    return render_template("registerresult.html", username=request.form["username"])