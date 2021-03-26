from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

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


@app.route("/")
def index():
    return render_template("index.html")

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
        return "old password incorrect"
    return myaccount()


@app.route("/registerform")
def registerform():
    return render_template("registerform.html")


@app.route("/salesadform")
def postsalesad():
    return render_template("salesadform.html")

@app.route("/insertsalesad", methods=["POST"])
def insertsalesad():
    author = session["username"]
    title = request.form["title"]
    content = request.form["content"]
    price_in_cents = int(float(request.form["price"])*100)

    sql = "INSERT INTO sales_ads (author, title, content, price_in_cents) VALUES (:author, :title, :content, :price_in_cents)"
    db.session.execute(sql, {"author":author, "title":title, "content":content, "price_in_cents":price_in_cents})
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
        return "User name already taken"
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/loginresult", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT * from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return "No user with that name"
    elif not check_password_hash(user["password"], password):
        return "Wrong password"
    session["username"] = username
    session["id"] = user["id"]
    print(session["id"])
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

