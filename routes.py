from app import app
from os import getenv, urandom
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session, abort
import messages, sales_ads, users, tags

@app.route("/searchresult", methods=["GET"])
def searchresult():
    query = request.args["query"]
    sales_ads_list = sales_ads.search(query)
    return render_template("searchresult.html", sales_ads=sales_ads_list)

@app.route("/advancedsearchresult", methods=["GET"])
def advancedsearchresult():
    author = request.args["author"]
    title = request.args["title"]
    content = request.args["content"]
    lowestprice = -99999999
    if len(request.args["lowestprice"]) >0:
        lowestprice = int(request.args["lowestprice"])*100
    highestprice= 99999999
    if len(request.args["highestprice"]) >0:
        highestprice = int(request.args["highestprice"])*100
    sales_ads_list = sales_ads.advancedsearch(author, title, content, highestprice, lowestprice)
    return render_template("searchresult.html", sales_ads=sales_ads_list)

@app.route("/editsalesadform/<int:id>", methods=["GET"])
def editsalesadform(id):
    if session["id"] != sales_ads.get_ads_user_id(id) and not session["admin"]:
        return notification("Error: This is not your ad to edit")
    ad = sales_ads.get_ad(id)
    ads_tags = tags.get_ads_tags(id)
    return render_template("editsalesadform.html", ad=ad, tags=ads_tags)

@app.route("/updatesalesad/<int:id>", methods=["GET", "POST"])
def updatesalesad(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if session["id"] != sales_ads.get_ads_user_id(id) and not session["admin"]:
        return notification("Error: This is not your ad to edit")
    if len(request.form["title"].strip()) == 0:
        return notification("Error: Title cannot be empty")
    if len(request.form["price"].strip()) == 0:
        return notification("Error: Price cannot be empty")
    title = request.form["title"]
    content = request.form["content"]
    tagsString = request.form["tags"]
    price_in_cents = int(float(request.form["price"])*100)
    sales_ads.update_ad(id, title, content, price_in_cents)
    tags.update_tags(tagsString, id)
    return redirect("/adpage/"+str(id))

@app.route("/advancedsearchform")
def advancedsearchform():
    return render_template("advancedsearchform.html")

@app.route("/deletemessage/<int:id>", methods=["GET", "POST"])
def deletemessage(id):
    user_id = messages.get_messages_user_id(id)
    if user_id == None:
        return notification("Error: No message to delete")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if user_id == session["id"] or session["admin"]:
        ad_id = messages.delete_message(id)
        return redirect("/adpage/"+str(ad_id))
    else:
        return notification("Error: Not your message or ad")

@app.route("/deleteaccountasadmin/<int:id>", methods=["GET", "POST"])
def deleteaccountasadmin(id):
    if users.get_user(id) == None:
        return notification("Error: No user")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if session["admin"]:
        users.delete_user(id)
        return notification("Success: User's Account deleted")
    else:
        return notification("Error: Not an admin")


@app.route("/deleteaccount", methods=["GET", "POST"])
def deleteaccount():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    password = users.get_password(session["id"])
    if check_password_hash(password, request.form["passworddel"]):
        users.delete_user(session["id"])
        purgeSession()
        return notification("Success: Account deleted")
    else:
        return notification("Error: Wrong password")
    
@app.route("/deletead/<int:id>", methods=["GET", "POST"])
def deletead(id):
    if sales_ads.get_ad(id) == None:
        return notification("Error: No ad")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    user_id = sales_ads.get_ads_user_id(id)
    if session["id"]==user_id or session["admin"]:
        sales_ads.delete_ad(id)
        return notification("Success: Ad deleted")
    else:
        return notification("Error: Not your ad")
    

@app.route("/notification/<string:notification>")
def notification(notification):
    return render_template("notification.html", notification=notification)

@app.route("/tag/<int:id>", methods=["GET"])
def tag(id):
    tag = tags.get_tag(id)
    if (not tag):
        return notification("Error: No such tag")
    return render_template("tag.html", tag = tag, ads=tags.get_tags_ads(id))

@app.route("/adpage/<int:id>", methods=["GET"])
def adpage(id):
    ad = sales_ads.get_ad(id)
    if ad == None:
        return notification("Error: No ad")
    ads_messages = messages.get_all_ads_messages(ad["id"])
    ads_tags = tags.get_ads_tags(id)
    return render_template("adpage.html", ad=ad, messages=ads_messages, tags=ads_tags)

@app.route("/")
def index():
    if len(session) != 0:
        if users.get_user(session["id"]) == None:
            purgeSession()
    tag_list = tags.get_all_tags_with_count()
    return render_template("index.html", tag_list=tag_list)

@app.route("/loginform")
def loginform():
    return render_template("loginform.html")

@app.route("/myaccount")
def myaccount():
    if len(session) == 0:
        return notification("Error: You are not logged in.")
    return account(session["id"])

@app.route("/account/<int:id>", methods=["GET"])
def account(id):
    user = users.get_user(id)
    if (user == None):
        if users.get_user(session["id"]) == None:
            purgeSession()
        return notification("Error: No user")
    ads = sales_ads.list_users_ads(id)
    return render_template("account.html", id=id, user=user, ads=ads)

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

@app.route("/makeadmin/<int:id>", methods=["POST"])
def makeadmin(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if session["admin"]:
       users.make_admin(id)
    return notification("Success: You made the user an admin")

@app.route("/postmessage/<int:ad_id>", methods=["GET", "POST"])
def postmessage(ad_id):
    if sales_ads.get_ad(ad_id) == None:
        return notification("Error: No ad")
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

@app.route("/insertsalesad", methods=["POST", "GET"])
def insertsalesad():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if len(request.form["title"].strip()) == 0:
        return notification("Error: Title cannot be empty")
    if len(request.form["price"].strip()) == 0:
        return notification("Error: Price cannot be empty")   
    title = request.form["title"]
    content = request.form["content"]
    tagsString = request.form["tags"]
    price_in_cents = int(float(request.form["price"])*100)
    id = sales_ads.insert_ad(session["username"], title, content, price_in_cents, session["id"])
    tags.insert_tags(tagsString, id)
    return redirect("/adpage/"+str(id))

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
    return notification("Success: New account registered. Please log in.")

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
    session["admin"] = user["admin"]
    session["csrf_token"] = urandom(16).hex()
    return notification("Success: Logged in")

@app.route("/logout")
def logout():
    purgeSession()
    return redirect("/")

def purgeSession():
    del session["username"]
    del session["id"]
    del session["admin"]
    del session["csrf_token"]