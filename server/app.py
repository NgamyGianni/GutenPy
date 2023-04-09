import redis, json, sqlite3, ast, re
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

app = Flask(__name__)
CORS(app, support_credentials=True)

def LtoDict(L):
	d = dict()

	for (title, iden, downloads, count) in L:
		if title in d:
			d[title][2] += count
		else:
			d[title] = [iden, downloads, count]

	return d

def search(s):
	# Functions
	score = lambda title, d : (0.01 * d[title][1]) + d[title][2]

	# book_info :: (title, id, downloads, word_count)
 	# Request -> [[book_info]]
	LL = [[json.loads(e) for e in r.lrange(word.lower(), 0, -1)] for word in s.split(" ")]
	LLtitles = [[e[0] for e in L] for L in LL]

	# [[book_info]] -> [book_info]
	L = [e for L in LL for e in L]
	Ltitles = [e[0] for e in L]
	titlesFiltered = [e for e in Ltitles if [e in LLtitles[i] for i in range(len(LLtitles))].count(False) == 0]
 
	# filter 
	#f = list(filter(lambda x: L.count(x) == len(LL), L))
	f = list(filter(lambda x: x[0] in titlesFiltered, L))
 
	# L -> dict{title : [id, downloads, count]}
	d = LtoDict(f)
 
	# ResultList 
	results = [(d[title][0], title, score(title, d)) for title in d]

	# Sorted List
	results = sorted(results, key=lambda x : score(x[1], d), reverse=True)

	return results

@app.route("/", methods=["GET"])
@cross_origin(supports_credentials=True)
def simple_search():
	req = request.args.get("search")
	if req is None: return {"result" : []}
 
	# Results :: [(id, title, score)]
	return {"results" : search(req)}

@app.route("/re", methods=["GET"])
@cross_origin(supports_credentials=True)
def regex_search():
	req = request.args.get("search")
	if req is None: return {"result" : []}

	# string -> regex
	regex = re.compile(req)

	# words if regex match
	keys = [key.decode('utf-8') for key in r.keys()]
	filtered_words = list(filter(lambda key : re.match(regex, key), keys))

	res = set()
	for word in filtered_words : 
		res = res.union(search(word))

	# Sorted List
	results = sorted(res, key=lambda x : x[2], reverse=True)

	return {"results" : results}

@app.route("/sugg", methods=["GET"])
@cross_origin(supports_credentials=True)
def sugg():
	req = request.args.get('id')
	if req is None: return {"result" : []}

	conn = sqlite3.connect('books.db')
	cursor = conn.cursor()

	# i, next, closeness, betweenness
	cursor.execute("SELECT next FROM graphe WHERE i="+req)
	rows = cursor.fetchone()
 
	ids = ast.literal_eval(rows[0])

	titles = []
	for id in ids:
		cursor.execute("SELECT title from book where i=" + str(id))
		title = cursor.fetchone()
		titles.append(title)
 
	conn.close()
 
	res = [[ids[i], titles[i][0]] for i in range(len(titles))]

	return jsonify({"results" : res})

@app.route("/recommend", methods=["GET"])
@cross_origin(supports_credentials=True)
def recommend():
	conn = sqlite3.connect('books.db')
	cursor = conn.cursor()

	# i, next, closeness, betweenness
	cursor.execute("SELECT g.i, b.title FROM graphe g, book b WHERE g.i=b.i ORDER BY closeness DESC LIMIT 5")
	rows = cursor.fetchall()
 
	conn.close()

	return jsonify({"results" : [(row[0], row[1]) for row in rows]})