import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO links (link) VALUES (?)",
            ('First Link',)
            )

cur.execute("INSERT INTO links (link) VALUES (?)",
            ('Second Link',)
            )

connection.commit()
connection.close()
