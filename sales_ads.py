from db import db
from datetime import datetime, timezone

def search(query):
    sql = "SELECT * FROM sales_ads WHERE title LIKE :query ORDER BY created_at DESC"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    sales_ads = result.fetchall()
    return sales_ads

def get_ads_user_id(id):
    sql = "SELECT user_id from sales_ads WHERE id = :id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user[0]

def delete_ad(id):
    sql = "DELETE FROM sales_ads WHERE id = :id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def get_ad(id):
    sql = "SELECT * from sales_ads WHERE id = :id"
    result = db.session.execute(sql, {"id":id})
    ad = result.fetchone()
    return ad

def insert_ad(author, title, content, price_in_cents, user_id):
    dt = datetime.now(timezone.utc)
    sql = "INSERT INTO sales_ads (author, title, content, price_in_cents, user_id, created_at, last_modified) VALUES (:author, :title, :content, :price_in_cents, :user_id, :dt, :dt)"
    db.session.execute(sql, {"author":author, "title":title, "content":content, "price_in_cents":price_in_cents, "user_id":user_id, "dt":dt})
    db.session.commit()