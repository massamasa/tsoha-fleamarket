CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, joined_at TIMESTAMP, admin BOOLEAN);
CREATE TABLE sales_ads (id SERIAL PRIMARY KEY,  author TEXT,  title TEXT, content TEXT, price_in_cents INTEGER, created_at TIMESTAMP, last_modified TIMESTAMP, user_id INT, CONSTRAINT fk_user
  FOREIGN KEY(user_id) 
      REFERENCES users(id) 
        ON DELETE CASCADE);
CREATE TABLE messages (ad_id INTEGER, user_id INTEGER, author_name TEXT, content TEXT, private BOOLEAN, created_at TIMESTAMP, id SERIAL PRIMARY KEY, 
CONSTRAINT fk_user
  FOREIGN KEY(user_id) 
      REFERENCES users(id) 
        ON DELETE CASCADE,
CONSTRAINT fk_ad
  FOREIGN KEY(ad_id) 
      REFERENCES sales_ads(id) 
        ON DELETE CASCADE);
CREATE TABLE tags (id SERIAL PRIMARY KEY, tag_name TEXT);
CREATE TABLE ads_tags (tag_id INTEGER, ad_id INTEGER, tag_name TEXT, 
CONSTRAINT fk_tag
  FOREIGN KEY(tag_id) 
      REFERENCES tags(id) 
        ON DELETE CASCADE,
CONSTRAINT fk_ad
  FOREIGN KEY(ad_id) 
      REFERENCES sales_ads(id) 
        ON DELETE CASCADE);
