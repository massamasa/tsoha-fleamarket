from db import db
from datetime import datetime, timezone

def insert_user(username, password):
    dt = datetime.now(timezone.utc)
    sql = "INSERT INTO users (username, password, joined_at, admin) VALUES (:username, :password, :dt, false)"
    db.session.execute(sql, {"username":username, "password":password, "dt":dt})
    db.session.commit()

def get_password(user_id):
    sql = "SELECT password from users WHERE id = :id"
    result = db.session.execute(sql, {"id":user_id})
    user = result.fetchone()
    return user[0]

def check_username(username):
    sql = "SELECT * from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user != None

def check_admin(id):
    sql = "SELECT admin from users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user[0]

def set_password(user_id, newpasswordhash):
    sql = "UPDATE users SET password =:newpassword WHERE id=:id"
    db.session.execute(sql, {"newpassword":newpasswordhash, "id":user_id})
    db.session.commit()

def make_admin(user_id):
    sql = "UPDATE users SET admin = true WHERE id=:id"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def delete_user(user_id):
    sql = "DELETE FROM users WHERE id = :id"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def get_user(user_id):
    sql = "SELECT * from users WHERE id=:id"
    result = db.session.execute(sql, {"id":user_id})
    user = result.fetchone()
    return user

def get_user_by_username(username):
    sql = "SELECT * from users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user