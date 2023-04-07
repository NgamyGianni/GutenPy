import ast, sqlite3, json, networkx as nx


def jaccard(set1, set2) : 
	intersection = len(set1.intersection(set2))
	union = len(set1.union(set2))

	return 1 - (intersection/union)

# Connect db
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM book")
rows = cursor.fetchall()

threshold = 0.5
books = rows
d = {i : [] for (_, _, i, _, _) in rows}

_, _, _, _, words1 = rows[0]
words1 = ast.literal_eval(words1)

_, _, _, _, words2 = rows[1]
words2 = ast.literal_eval(words2)

for book in books:
	_, _, i1, _, words1 = book
	words1 = ast.literal_eval(words1)

	for otherBook in books:
		_, _, i2, _, words2 = otherBook
		words2 = ast.literal_eval(words2)
		if book != otherBook and not((i1, i2) in d[i1] or (i2, i1) in d[i1]):
			
			j = jaccard(set(words1.keys()), set(words2.keys()))
			if j <= threshold:
				d[i1].append((i1, i2))
				d[i2].append((i1, i2))

nodes = list(d.keys())
edges = {e for L in d.values() for e in L}

print(nodes, edges)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# {id : centrality}
betweenness_centralities = nx.betweenness_centrality(G)
closeness_centralities = nx.closeness_centrality(G)
edges = lambda key : [a if b == key else b for (a, b) in d[key]]

for book in books:
	_, _, i1, _, _ = book
	nextBooks = json.dumps(edges(i1))
	close = closeness_centralities[i1]
	between = betweenness_centralities[i1]

	cursor.execute('INSERT INTO graphe (i, next, closeness, betweenness) VALUES (?, ?, ?, ?)',
							   (i1, nextBooks, close, between))
	conn.commit()

# Deconnect db
conn.close()