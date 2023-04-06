import redis, json, sqlite3, ast
from flask import Flask, request
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

@app.route("/", methods=["GET"])
@cross_origin(supports_credentials=True)
def home():
	
	# Functions
	score = lambda title, d : (0.01 * d[title][1]) + d[title][2]

	req = request.args.get("search")
	if req is None: return {"result" : []}

	# book_info :: (title, id, downloads, word_count)
 	# Request -> [[book_info]]
	LL = [[json.loads(e) for e in r.lrange(word.lower(), 0, -1)] for word in req.split(" ")]
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
 
	# Results :: [(id, title, score)]
	return {"results" : results}

@app.route("/all", methods=["GET"])
@cross_origin(supports_credentials=True)
def state():	return {"keys" : [key.decode('utf-8') for key in r.keys()]}

@app.route("/suggest", methods=["GET"])
@cross_origin(supports_credentials=True)
def sugg():
	req = request.args.get('search')
	if req is None: return {"result" : []}
	
	wordResults = lambda word : [json.loads(e) for e in r.lrange(word.lower(), 0, -1)]
	titles = lambda word : {e[0] for e in wordResults(word)}
	jaccard = lambda w1, w2 : 1 - (len(titles(w1).intersection(titles(w2))) / len(titles(w1).union(titles(w2))))
	
	res = dict()
	
	for word in r.keys():
		tmpWord = word.decode('utf-8')
		if tmpWord != req:
			res[tmpWord] = jaccard(req, tmpWord)

	sorted_words_by_jaccard = sorted(res.items(), key=lambda x:x[1], reverse=True)
	converted_dict = dict(sorted_words_by_jaccard)
 
	return {"results" : str(converted_dict)}

@app.route("/sugg", methods=["GET"])
@cross_origin(supports_credentials=True)
def sugg2():
	req = request.args.get('id')
	if req is None: return {"result" : []}

	conn = sqlite3.connect('books.db')
	cursor = conn.cursor()

	# i, next, closeness, betweenness
	cursor.execute("SELECT next FROM graphe WHERE i = ?", req)
	rows = cursor.fetchone()
 
	conn.close()

	return {"results" : str(rows[0])}