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

def get_user_by_id(id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_details WHERE id = ?",(id,))
        return cursor.fetchone()
    
def get_user_by_email(email):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_details WHERE email = ?",(email,)) 
        return cursor.fetchone() 


def create_table():
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS topics(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT NOT NULL,
                            progress REAL NOT NULL,
                            user_id INTEGER NOT NULL
                            )""")
    
def add_topic(topic,progress,user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO topics(topic,progress,user_id) VALUES(?,?,?)",(topic,progress,user_id))

def view_topics(user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE user_id = ?",(user_id,))
        c=cursor.fetchall()
        return c

def update_topic(id,topic,progress,user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE topics SET topic=?, progress=? WHERE id= ? AND user_id = ?",(topic,progress,id,user_id))

def delete_topic(id , user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM topics WHERE id = ? AND user_id = ?",(id,user_id))

def search_topic(topic,user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE topic LIKE ? AND user_id = ?",('%'+topic+'%',user_id))
        result = cursor.fetchall()
        return result
def get_topic(id,user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id=? AND user_id = ?",(id,user_id))
        return cursor.fetchone()
def topic_exists(topic,user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE topic = ? AND user_id = ?",(topic,user_id))
        result = cursor.fetchone()
        return result != None



