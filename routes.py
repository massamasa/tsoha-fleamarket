from app import app
from os import getenv, urandom
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session, abort
import messages, sales_ads, users

@app.route("/searchresult", methods=["GET"])
def searchresult():
    query = request.args["query"]
    sales_ads_list = sales_ads.search(query)
    return render_template("searchresult.html", sales_ads=sales_ads_list)

@app.route("/deletemessage/<int:id>", methods=["GET", "POST"])
def deletemessage(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    user_id = messages.get_messages_user_id(id)
    if user_id == session["id"]:
        messages.delete_message(id)
        return notification("Success: Message deleted")
    else:
        return notification("Error: Not your message or ad")



@app.route("/deleteaccount", methods=["GET", "POST"])
def deleteaccount():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    password = users.get_password(session["id"])
    if check_password_hash(password, request.form["passworddel"]):
        users.delete_user(session["id"])
        del session["id"]
        del session["username"]
        return notification("Success: Account deleted")
    else:
        return notification("Error: Wrong password")
    
@app.route("/deletead/<int:id>", methods=["GET", "POST"])
def deletead(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    user_id = sales_ads.get_ads_user_id(id)
    if (session["id"]==user_id):
        sales_ads.delete_ad(id)
        return notification("Success: Ad deleted")
    else:
        return notification("Error: Not your ad")
    

@app.route("/notification/<string:notification>")
def notification(notification):
    return render_template("notification.html", notification=notification)

@app.route("/adpage/<int:id>", methods=["GET"])
def adpage(id):
    ad = sales_ads.get_ad(id)
    ads_messages = messages.get_all_ads_messages(ad["id"])
    return render_template("adpage.html", ad=ad, messages=ads_messages)

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
    user = users.get_user(id)
    return render_template("account.html", id=id, user=user)

@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    password = users.get_password(session["id"])
    if check_password_hash(password, request.form["passwordold"]):
        if (request.form["passwordnew"] == request.form["passwordnewre"]):
           users.set_password(session["id"], generate_password_hash(request.form["passwordnew"]))
        else:
            return notification("Error: Passwords do not match")
    else:
        return notification("Error: Old password incorrect")
    return notification("Success: Password changed")

@app.route("/postmessage/<int:ad_id>", methods=["POST"])
def postmessage(ad_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    private = request.form["privateRadio"]=="1"
    content = request.form["content"]
    if len(content.strip()) == 0:
        return notification("Error: A message must have content")
    messages.insert_message(ad_id, private, content, session["id"], session["username"])
    return redirect("/adpage/"+str(ad_id))


@app.route("/registerform")
def registerform():
    return render_template("registerform.html")


@app.route("/salesadform")
def postsalesad():
    return render_template("salesadform.html")

@app.route("/insertsalesad", methods=["POST"])
def insertsalesad():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if len(request.form["title"].strip()) == 0:
        return notification("Error: Title cannot be empty")
    if len(request.form["price"].strip()) == 0:
        return notification("Error: Price cannot be empty")   
    title = request.form["title"]
    content = request.form["content"]
    price_in_cents = int(float(request.form["price"])*100)
    sales_ads.insert_ad(session["username"], title, content, price_in_cents, session["id"])
    return redirect("/")

@app.route("/registerresult", methods=["POST", "GET"])
def registerresult():
    username = request.form["username"]
    password = request.form["password"]
    if len(username.strip())==0:
        return notification("Error: Username cannot be empty")
    if len(password) == 0:
        return notification("Error: Password required")
    if users.check_username(username):
        return notification("Error: User name already taken.")
    hash_value = generate_password_hash(password)
    users.insert_user(username, hash_value)
    return notification("Success: New account registered.")

@app.route("/loginresult", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.get_user_by_username(username)
    if user == None:
        return notification("Error: No user with that name")
    elif not check_password_hash(user["password"], password):
        return notification("Error: Wrong password")
    session["username"] = username
    session["id"] = user["id"]
    session["csrf_token"] = urandom(16).hex()
    return notification("Success: Logged in")

@app.route("/logout")
def logout():
    del session["username"]
    del session["id"]
    del session["csrf_token"]
    return redirect("/")

