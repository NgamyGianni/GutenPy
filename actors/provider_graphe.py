import redis, json, pika, sys, os, sqlite3

def main():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='graphe')

	def callback(ch, method, properties, body):
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

	channel.basic_consume(queue='graphe', on_message_callback=callback, auto_ack=True)

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
