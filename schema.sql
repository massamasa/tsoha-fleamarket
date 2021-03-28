CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE sales_ads (id SERIAL PRIMARY KEY,  author TEXT,  title TEXT, content TEXT, price_in_cents INTEGER, created_at TIMESTAMP, last_modified TIMESTAMP, user_id INT, CONSTRAINT fk_user
  FOREIGN KEY(user_id) 
      REFERENCES users(id) 
        ON DELETE CASCADE);
