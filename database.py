import sqlite3
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
        cursor.execute("SELECT * FROM topics WHERE topic = ?",(topic,))
        result = cursor.fetchone()
        if result is None:
            return "topic is not present..."
        else:
            return result
def get_topic(id):
    with sqlite3.connect("learning.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id=?",(id,))
        return cursor.fetchone()