import sqlite3
def user_login():
    with sqlite3.connect("learning.db") as conn:
        cursor =conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS login_details(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       email TEXT NOT NULL,
                       password TEXT NOT NULL
                       )""")

def add_user(name,email,password):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_details(name,email,password) VALUES(?,?,?)",(name,email,password))

def email_exists(email):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_details WHERE email = ?",(email,))
        result = cursor.fetchone()
        return (result is not None)
    
def email_login(email,password):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_details WHERE email = ? AND password = ?",(email,password))
        return cursor.fetchone()

def get_user_by_id(id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_details WHERE id = ?",(id,))
        return cursor.fetchone()


def create_table():
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS topics(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT NOT NULL,
                            progress REAL NOT NULL 
                            )""")
    
def add_topic(topic,progress):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO topics(topic,progress) VALUES(?,?)",(topic,progress))

def view_topics():
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics")
        c=cursor.fetchall()
        return c

def update_topic(id,topic,progress):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE topics SET topic=?, progress=? WHERE id=?",(topic,progress,id))

def delete_topic(id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM topics WHERE id = ?",(id,))

def search_topic(topic):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE topic LIKE ?",('%'+topic+'%',))
        result = cursor.fetchall()
        return result
def get_topic(id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id=?",(id,))
        return cursor.fetchone()
def topic_exists(topic):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE topic = ?",(topic,))
        result = cursor.fetchone()
        return result != None
