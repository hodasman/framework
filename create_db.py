import sqlite3

con = sqlite3.connect('/Users/Macintosh/Desktop/hodas_framework/base.sqlite')
cur = con.cursor()
with open('/Users/Macintosh/Desktop/hodas_framework/create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
