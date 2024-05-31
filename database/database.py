import psycopg2

# CONNECT TO THE DATABASE
def connect():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )

# CREATE TABLE IF IT DOESN'T EXIST
def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users_details_ecommerce (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL, 
                    password VARCHAR(100) NOT NULL
                )
            """)
            conn.commit()
        
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users_liked_ecommerce_products (
                    id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_asin VARCHAR(255) NOT NULL,
                    product_title VARCHAR(255) NOT NULL,
                    product_price VARCHAR(255) NOT NULL,
                    product_star_rating VARCHAR(255) NOT NULL,
                    product_url TEXT NOT NULL,
                    product_photo TEXT NOT NULL,
                    delivery VARCHAR(255) NOT NULL,
                    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users_details_ecommerce(id),
                    CONSTRAINT unique_user_product UNIQUE (user_id, product_asin)
                )
            """)
            conn.commit()

# FETCHES USERNAME FROM THE DATABASE
def username_in_database(name, password):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM users_details_ecommerce WHERE username = %s""", (name,))
            user = cur.fetchone()  # This fetches the user

    # This checks if there is a user and the password matches
    if user and user[2] == password:
        return True
    else:
        return False

# ADD USERS DETAILS TO THE DATABASE
def insert_into_database(username, password):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users_details_ecommerce (username, password) VALUES (%s, %s)", 
                        (username, password))
            conn.commit()

# USED TO GET THE USER ID FROM THE DATABASE
def get_user_id(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users_details_ecommerce WHERE username = %s", (username,))
            result = cur.fetchone()
            if result is not None:
                return result[0]
            else:
                raise ValueError("User with username '{}' not found.".format(username))

# ADD TO LIKE TABLE
def add_to_like_table(user_id, product):
    with connect() as conn:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO users_liked_ecommerce_products (
                    user_id, product_asin, product_title, product_price, 
                    product_star_rating, product_url, product_photo, delivery
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id, product_asin) DO NOTHING
            """, (
                user_id, 
                product["product_asin"], 
                product["product_title"], 
                product["product_price"], 
                product["product_star_rating"], 
                product["product_url"], 
                product["product_photo"], 
                product["product_delivery"]
            ))
            conn.commit()

# REMOVE FROM LIKE TABLE
def remove_from_like_table(user_id, product_asin):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM users_liked_ecommerce_products
                WHERE user_id = %s AND product_asin = %s
            """, (user_id, product_asin))
            conn.commit()


def get_user_liked_products(user_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT product_asin, product_title, product_price, 
                               product_star_rating, product_url, 
                               product_photo, delivery 
                        FROM users_liked_ecommerce_products 
                        WHERE user_id = %s
                        """, (user_id,))
            
            items = cur.fetchall()

            return items
