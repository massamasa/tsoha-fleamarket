from db import db

def add_tag(tag_name): # committed in insert_tags
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
    tags_list = tagsString.split()
    for tag_name in tags_list:
        if len(tag_name.strip()) > 0:
            tag_id = add_tag(tag_name)
            join_ad_tag(ad_id, tag_id)
            db.session.commit()

def update_tags(tagsString, ad_id): # committed in insert_tags
    sql= "DELETE FROM ads_tags WHERE ads_tags.ad_id = :ad_id"
    db.session.execute(sql, {"ad_id":ad_id})
    insert_tags(tagsString, ad_id)


def get_all_tags_with_count():
    sql = "SELECT tags.tag_name, ads_tags.tag_id, COUNT(ads_tags.tag_id) AS count_tag \
        FROM ads_tags INNER JOIN tags ON tags.id = ads_tags.tag_id \
            GROUP BY ads_tags.tag_id, tags.tag_name ORDER BY count_tag DESC"
    result = db.session.execute(sql, {})
    return result.fetchall()

def get_tags_ads(id):
    sql = "SELECT sales_ads.* FROM sales_ads \
        INNER JOIN ads_tags ON ads_tags.ad_id = sales_ads.id \
            INNER JOIN tags ON ads_tags.tag_id = :id \
                GROUP BY sales_ads.id ORDER BY sales_ads.last_modified DESC"

    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_tag(id):
    sql = "SELECT * from tags WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_ads_tags(id):
    sql = "SELECT tags.* FROM tags \
        INNER JOIN ads_tags ON ads_tags.tag_id = tags.id \
            INNER JOIN sales_ads ON ads_tags.ad_id = :id \
                GROUP BY tags.id ORDER BY tags.tag_name"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()