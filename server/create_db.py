import sqlite3, json, ast

def createBooks():
	# Connexion à la base de données
	conn = sqlite3.connect('books.db')
	cursor = conn.cursor()

	# Création de la table
	cursor.execute('''
		CREATE TABLE book (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			i INTEGER NOT NULL,
			downloads INTEGER NOT NULL,
			word TEXT NOT NULL,
			CONSTRAINT unique_row UNIQUE (i)
		)
	''')

	# Fermeture de la connexion à la base de données
	conn.close()

def createGrapheDb():
	# Connexion à la base de données
	conn = sqlite3.connect('books.db')
	cursor = conn.cursor()

	# Création de la table
	cursor.execute('''
		CREATE TABLE graphe (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			i INTEGER NOT NULL,
			next TEXT NOT NULL,
			closeness FLOAT NOT NULL,
			betweenness FLOAT NOT NULL,
			CONSTRAINT unique_row UNIQUE (i)
		)
	''')

	# Fermeture de la connexion à la base de données
	conn.close()
"""
# Ouvrir une connexion à la base de données
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

title = "heha"
i = 15
downloads = 5000
word_dict = str({"hello" : 10})

cursor.execute('INSERT INTO book (title, i, downloads, word) VALUES (?, ?, ?, ?)',
						   (title, i, downloads, word_dict))
conn.commit()
conn.close()"""

"""createBooks()
createGrapheDb()
"""

conn = sqlite3.connect('books.db')
cursor = conn.cursor()

title = "alice"
cursor.execute("SELECT * FROM graphe")
rows = cursor.fetchall()
print(rows)

conn.close()