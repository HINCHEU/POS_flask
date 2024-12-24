import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
''')
# Create products table
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        Cost INTEGER NOT NULL,
        price REAL NOT NULL,
        image TEXT,
        current_stock INTEGER NOT NULL,
        FOREIGN KEY (category) REFERENCES categories(id)
    )
''')
# Create Gender table
c.execute('''
    CREATE TABLE IF NOT EXISTS Gender (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

# Create Users table with a foreign key to Gender
c.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        profile TEXT,
        name TEXT NOT NULL,
        gender_id INTEGER,
        role TEXT,
        email TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        password TEXT,
        FOREIGN KEY (gender_id) REFERENCES Gender(id)
    )
''')
# Insert gender options
c.execute("INSERT INTO Gender (name) VALUES ('M')")
c.execute("INSERT INTO Gender (name) VALUES ('F')")
c.execute("INSERT INTO Gender (name) VALUES ('Other')")
conn.commit()
conn.close()
