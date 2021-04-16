from db import db
from datetime import datetime, timezone

def search(query):
    sql = "SELECT * FROM sales_ads WHERE title LIKE :query ORDER BY created_at DESC"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    sales_ads = result.fetchall()
    return sales_ads

def advancedsearch(author, title, content, highestprice, lowestprice):
    sql = "SELECT * FROM sales_ads WHERE (author LIKE :author) AND (title LIKE :title) AND (content LIKE :content) AND (price_in_cents <= :highestprice) AND (price_in_cents >= :lowestprice) ORDER BY created_at DESC"
    result = db.session.execute(sql, {"author":"%"+author+"%","title":"%"+title+"%", "content":"%"+content+"%", "highestprice":highestprice, "lowestprice":lowestprice})
    sales_ads = result.fetchall()
    return sales_ads

def list_users_ads(id):
    sql = "SELECT * FROM sales_ads WHERE user_id = :id ORDER BY created_at DESC"
    result = db.session.execute(sql, {"id":id})
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
    sql = "INSERT INTO sales_ads (author, title, content, price_in_cents, user_id, created_at, last_modified) \
        VALUES (:author, :title, :content, :price_in_cents, :user_id, :dt, :dt) RETURNING id"
    ad = db.session.execute(sql, {"author":author, "title":title, "content":content, "price_in_cents":price_in_cents, "user_id":user_id, "dt":dt})
    db.session.commit()
    return ad.fetchone()[0]