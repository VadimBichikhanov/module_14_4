import sqlite3

def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        image TEXT
    )
    ''')
     # Добавление записей в таблицу Products
    products = [
        ("Apple", "Свежее яблоко", 100, "images/apple.jpg"),
        ("Banana", "Спелый банан", 200, "images/banana.jpg"),
        ("Orange", "Апельсин", 300, "images/orange.jpg"),
        ("Grapes", "Виноград", 400, "images/grapes.jpg")
    ]

    cursor.executemany('''
    INSERT INTO Products (title, description, price, image) VALUES (?, ?, ?, ?)
    ''', products)

    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    conn.close()
    return products