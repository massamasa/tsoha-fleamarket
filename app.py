from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/searchresult", methods=["GET"])
def searchresult():
    query = request.args["query"]
    sql = "SELECT * FROM sales_ads WHERE title LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    sales_ads = result.fetchall()
    return render_template("searchresult.html", sales_ads=sales_ads)

@app.route("/notification/<string:notification>")
def notification(notification):
    return render_template("notification.html", notification=notification)

@app.route("/adpage/<int:id>", methods=["GET"])
def adpage(id):
    sql = "SELECT * from sales_ads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ad = result.fetchone()
    return render_template("adpage.html", ad=ad)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loginform")
def loginform():
    return render_template("loginform.html")

@app.route("/myaccount")
def myaccount():
    return account(session["id"])

@app.route("/account/<int:id>", methods=["GET"])
def account(id):
    sql = "SELECT * from users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return render_template("account.html", id=id, username=user["username"])

@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    sql = "SELECT password from users WHERE id=:id"
    result = db.session.execute(sql, {"id":session["id"]})
    user = result.fetchone()
    if check_password_hash(user["password"], request.form["passwordold"]):
        if (request.form["passwordnew"] == request.form["passwordnewre"]):
            sql = "UPDATE users SET password =:newpassword WHERE id=:id"
            newpasswordhash = generate_password_hash(request.form["passwordnew"])
            db.session.execute(sql, {"newpassword":newpasswordhash, "id":session["id"]})
            db.session.commit()
        else:
            return notification("Error: Passwords do not match")
    else:
        return notification("Error: Old password incorrect")
    return myaccount("Success: Password changed")


@app.route("/registerform")
def registerform():
    return render_template("registerform.html")


@app.route("/salesadform")
def postsalesad():
    return render_template("salesadform.html")

@app.route("/insertsalesad", methods=["POST"])
def insertsalesad():
    if len(request.form["title"]) == 0:
        return notification("Error: Title cannot be empty")
    print(request.form["price"])
    if len(request.form["price"]) == 0:
        return notification("Error: Price cannot be empty")   
    title = request.form["title"]
    content = request.form["content"]
    price_in_cents = int(float(request.form["price"])*100)
    dt = datetime.now(timezone.utc)
    sql = "INSERT INTO sales_ads (author, title, content, price_in_cents, user_id, created_at, last_modified) VALUES (:author, :title, :content, :price_in_cents, :user_id, :dt, :dt)"
    db.session.execute(sql, {"author":session["username"], "title":title, "content":content, "price_in_cents":price_in_cents, "user_id":session["id"], "dt":dt})
    db.session.commit()
    
    return redirect("/")

@app.route("/registerresult", methods=["POST"])
def registerresult():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT * from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user != None:
        return notification("Error: User name already taken.")
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return notification("Success: New account registered.")

@app.route("/loginresult", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT * from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return notification("Error: No user with that name")
    elif not check_password_hash(user["password"], password):
        return notification("Wrong password")
    session["username"] = username
    session["id"] = user["id"]
    print(session["id"])
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["id"]
    return redirect("/")

