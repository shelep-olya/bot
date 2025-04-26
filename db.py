import sqlite3

DATABASE_PATH = "diary.db"

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor() 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_schedule_entry(day, time, title):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedule (day, time, title) VALUES (?, ?, ?)", (day, time, title))
    conn.commit()
    conn.close()

def get_schedule():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedule")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_schedule_by_day(day):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedule WHERE day = ?", (day,))
    rows = cursor.fetchall()
    conn.close()
    return rows



