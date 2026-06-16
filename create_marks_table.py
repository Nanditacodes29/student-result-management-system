import sqlite3

conn = sqlite3.connect('students.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rollno TEXT,
    maths INTEGER,
    physics INTEGER,
    chemistry INTEGER
)
''')

conn.commit()
conn.close()

print("Marks table created!")