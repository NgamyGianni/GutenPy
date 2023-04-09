import redis, json, pika, sys, os, sqlite3

def main():
	pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
	r = redis.Redis(connection_pool=pool)
	pipe = r.pipeline()
 
	credentials = pika.PlainCredentials("provider", "provider")

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
	channel = connection.channel()

	channel.queue_declare(queue='book')
	channel.queue_declare(queue='graphe')
 
	def callback_graphe(ch, method, properties, body):
    		# Ouvrir une connexion à la base de données
		conn = sqlite3.connect('../server/books.db')
		cursor = conn.cursor()
     
		body = json.loads(body)
		title, i, downloads, word_dict = body
		word_dict = str(word_dict)

		print(" [x] Received %r" % i)

		# Persist
		cursor.execute('INSERT INTO book (title, i, downloads, word) VALUES (?, ?, ?, ?)',
						   (title, i, downloads, word_dict))
		conn.commit()
		conn.close()

	def callback(ch, method, properties, body):
		body = json.loads(body)
		title, i, downloads, word_dict = body

		print(" [x] Received %r" % i)

		# Persist
		for key in word_dict : pipe.rpush(key, json.dumps((title, i, downloads, word_dict[key])))
		pipe.execute()

	channel.basic_consume(queue='book', on_message_callback=callback, auto_ack=True)
	channel.basic_consume(queue='graphe', on_message_callback=callback_graphe, auto_ack=True)

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
