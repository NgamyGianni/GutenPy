import redis, json
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
			d[title][count] += count
		else:
			d[title] = [iden, downloads, count]

	return d

@app.route("/", methods=["GET"])
@cross_origin(supports_credentials=True)
def home():
	
	# Functions
	score = lambda title, d : (0.01 * d[title][1]) + d[title][2]
 
	req = request.args.get("search")

	# book_info :: (title, id, downloads, word_count)
 	# Request -> [[book_info]]
	LL = [[json.loads(e) for e in r.lrange(word.lower(), 0, -1)] for word in req.split(" ")]

	# [[book_info]] -> [book_info]
	L = [e for L in LL for e in L]
 
	# filter 
	f = list(filter(lambda x: L.count(x) == len(LL), L))
 
	# L -> dict{title : [id, downloads, count]}
	d = LtoDict(f)
 
	# ResultList 
	results = [(d[title][0], title, score(title, d)) for title in d]

	# Sorted List
	results = sorted(results, key=lambda x : score(x[1], d), reverse=True)
 
	# Results :: [(id, title, score)]
	return {"result" : results}
