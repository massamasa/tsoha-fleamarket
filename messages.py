from db import db
from datetime import datetime, timezone

def get_messages_user_id(id):
    sql = "SELECT user_id from messages WHERE id = :message_id"
    result = db.session.execute(sql, {"message_id":id})
    user = result.fetchone()
    return user[0]

def delete_message(id):
    sql = "DELETE FROM messages WHERE id = :message_id"
    db.session.execute(sql, {"message_id":id})
    db.session.commit()

def get_all_ads_messages(id):
    sql = "SELECT * FROM messages WHERE (ad_id = :id) ORDER BY created_at DESC"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()
    return messages

def insert_message(ad_id, private, content, user_id, username):
    dt = datetime.now(timezone.utc)
    sql = "INSERT INTO messages (ad_id, user_id, author_name, content, private, created_at) \
        VALUES (:ad_id, :user_id, :author_name, :content, :private, :dt)"
    db.session.execute(sql, {"ad_id":ad_id, "user_id":user_id, "author_name":username, "content":content, "private":private, "dt":dt})
    db.session.commit()