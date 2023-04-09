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

createBooks()
createGrapheDb()

"""conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
		SELECT closeness from graphe
''')
rows = cursor.fetchall()

print(rows)

# Fermeture de la connexion à la base de données
conn.close()"""