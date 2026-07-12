import sqlite3

DB_NAME = "crm.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        company TEXT,
        address TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        thickness TEXT,
        size TEXT,
        brand TEXT,
        color TEXT,
        unit TEXT,
        stock REAL DEFAULT 0,
        min_stock REAL DEFAULT 0,
        buy_price REAL DEFAULT 0,
        sell_price REAL DEFAULT 0,
        warehouse TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


def add_customer(name, phone, company, address):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers(name,phone,company,address) VALUES(?,?,?,?)",
            (name, phone, company, address),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        try:
            conn.close()
        except:
            pass
        return False


def get_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id,name,phone,company,address FROM customers ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return data


def search_customers(text):
    conn = get_connection()
    cur = conn.cursor()
    like = f"%{text}%"
    cur.execute(
        """SELECT id,name,phone,company,address
           FROM customers
           WHERE name LIKE ? OR phone LIKE ? OR company LIKE ? OR address LIKE ?
           ORDER BY id DESC""",
        (like, like, like, like),
    )
    data = cur.fetchall()
    conn.close()
    return data


def update_customer(customer_id, name, phone, company, address):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """UPDATE customers
               SET name=?, phone=?, company=?, address=?
               WHERE id=?""",
            (name, phone, company, address, customer_id),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        try:
            conn.close()
        except:
            pass
        return False


def delete_customer(customer_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    conn.close()
def get_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT id,name,category,thickness,size,brand,color,unit,stock,sell_price
    FROM products
    ORDER BY id DESC
    """)
    data=cur.fetchall()
    conn.close()
    return data

def search_products(text):
    conn=get_connection()
    cur=conn.cursor()
    like=f"%{text}%"
    cur.execute("""
    SELECT id,name,category,thickness,size,brand,color,unit,stock,sell_price
    FROM products
    WHERE name LIKE ? OR category LIKE ? OR brand LIKE ?
    ORDER BY id DESC
    """,(like,like,like))
    data=cur.fetchall()
    conn.close()
    return data

def update_product(pid,name,category,thickness,size,brand,color,unit,stock,min_stock,buy_price,sell_price,warehouse,description):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""
    UPDATE products SET
    name=?,category=?,thickness=?,size=?,brand=?,color=?,unit=?,
    stock=?,min_stock=?,buy_price=?,sell_price=?,warehouse=?,description=?
    WHERE id=?
    """,(name,category,thickness,size,brand,color,unit,stock,min_stock,buy_price,sell_price,warehouse,description,pid))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?",(pid,))
    conn.commit()
    conn.close()
