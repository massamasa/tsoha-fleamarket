from db import db

def add_tag(tag_name):
    sql = "SELECT id FROM tags WHERE tag_name = :tag_name"
    result = db.session.execute(sql, {"tag_name":tag_name})
    tag = result.fetchone()
    if tag == None:
        sql2 = "INSERT INTO tags (tag_name) VALUES (:tag_name) RETURNING id"
        result2 = db.session.execute(sql2, {"tag_name":tag_name})
        tag_id = result2.fetchone()[0]
        return tag_id
    else:
        return tag[0]



def join_ad_tag(ad_id, tag_id): # committed in insert_tags
    sql = "SELECT * FROM ads_tags WHERE (ad_id = :ad_id AND tag_id = :tag_id)"
    result = db.session.execute(sql, {"ad_id":ad_id, "tag_id":tag_id})
    ad_tag = result.fetchone()
    if ad_tag == None:
        sql = "INSERT INTO ads_tags (ad_id, tag_id) VALUES (:ad_id, :tag_id)"
        db.session.execute(sql, {"ad_id":ad_id, "tag_id":tag_id})

def insert_tags(tagsString, ad_id):
    tagss = tagsString.split()
    print(tagss)
    for tag_name in tagss:
        if len(tag_name.strip()) > 0:
            tag_id = add_tag(tag_name)
            print(tag_id)
            join_ad_tag(ad_id, tag_id)
            db.session.commit()

def get_all_tags_with_count():
    sql = "SELECT tags.tag_name, ads_tags.tag_id, COUNT(ads_tags.tag_id) AS count_tag \
        FROM ads_tags INNER JOIN tags ON tags.id = ads_tags.tag_id \
            GROUP BY ads_tags.tag_id, tags.tag_name ORDER BY count_tag DESC"
    result = db.session.execute(sql, {})
    return result.fetchall()