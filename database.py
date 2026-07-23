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

def update_password(email, password):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE login_details SET password=? WHERE email=?",(password, email))



def create_table():
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS topics(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            topic TEXT NOT NULL,
                            progress REAL NOT NULL,
                            category TEXT DEFAULT 'General',
                            user_id INTEGER NOT NULL
                            )""")
    
def add_topic(topic,progress,user_id,category):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO topics(topic,progress,category,user_id) VALUES(?,?,?,?)",(topic,progress,category,user_id))

def view_topics(user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE user_id = ?",(user_id,))
        c=cursor.fetchall()
        return c

def update_topic(id,topic,progress,user_id,category):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE topics SET topic=?, progress=? ,category=? WHERE id= ? AND user_id = ?",(topic,progress,category,id,user_id))

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

def get_statistics(user_id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM topics WHERE user_id=?",(user_id,))
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM topics WHERE progress=100 AND user_id=?",(user_id,))
        completed = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM topics WHERE progress>0 AND progress<100 AND user_id=?",(user_id,))
        in_progress = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM topics WHERE progress=0 AND user_id=?",(user_id,))
        not_started = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(progress) FROM topics WHERE user_id=?",(user_id,))
        overall_progress = cursor.fetchone()[0]
        if overall_progress is None:
            overall_progress = 0
        return {"total": total,"completed": completed,"in_progress": in_progress,"not_started": not_started,"overall_progress": round(overall_progress, 2)}


with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM login_details WHERE name = ?",("Anmol Saxena",))