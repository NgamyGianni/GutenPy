import requests, pika, json, sys, os

forbidden_words = []

# Cree un dictionnaire de (mot, occurence) 
#strToDictCount = lambda s : {e : s.count(e) for e in s.split(" ")} # n^2

# Verifie si un caractère est autorise
isGoodChar = lambda x : x in [chr(i) for i in list(range(97, 97+26)) + list(range(65, 65+26))] or x == " "

# Verifie si un mot est autorise
isGoodWord = lambda x : len(x) >= 4 and not(x in forbidden_words)

# Renvoie l'url gutendex d'une page
getUrl = lambda id :  "https://www.gutenberg.org/files/{}/{}-0.txt".format(id, id)

# Renvoie la page gutendex recherchee
getResponseText = lambda id : requests.get(getUrl(id)).text.lower()

# Retire les mauvais caractères et mots
cleanText = lambda text : " ".join(filter(isGoodWord, "".join(filter(isGoodChar, text)).split(" ")))

# Cree un dictionnaire avec les bons mots et leurs occurences
cleanTextToDico = lambda text : strToDictCount(text)

# Trie le dictionnaire par les valeurs decroissantes
sortedDicoCleanText = lambda dico : dict(sorted(dico.items(), key=lambda x:x[1], reverse=True))

# Text -> sortedDicoCleanText : global operation
textToSortedDicoCleanText = lambda text : sortedDicoCleanText(cleanTextToDico(cleanText(text)))


def strToDictCount(s : str):
	d = dict()
	txt = s.split(" ")

	for e in txt:
		if e in d:
			d[e] += 1
		else:
			d[e] = 1

	return d


def main():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='id')

	def send(body, title):

		connection = pika.BlockingConnection(
		    pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()

		channel.queue_declare(queue='book')

		channel.basic_publish(exchange='', routing_key='book', body=body)

		print(" [x] Sent " + title)
		connection.close()

	def callback(ch, method, properties, body):
		#body : str(id)
		body = json.loads(body)

		print(" [x] Received %r" % body)

		# Traitement
		response = requests.get("https://gutendex.com/books/" + str(body))
  
		if response.status_code == 200 :
			responseJson = response.json()	
			title = responseJson["title"]
			downloads = responseJson["download_count"]
   
			text = getResponseText(body)
			dico = textToSortedDicoCleanText(text)

			body = json.dumps((title, body, downloads, dico))

			send(body, title)

	channel.basic_qos(prefetch_count=2)
	channel.basic_consume(queue='id', on_message_callback=callback, auto_ack=True)

	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

