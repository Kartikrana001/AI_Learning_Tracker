import sqlite3
conn = sqlite3.connect("learning.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS topics(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    progress REAL NOT NULL 
                    )""")
conn.commit()
conn.close()