import redis, json, pika, sys, os

def main():
	pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
	r = redis.Redis(connection_pool=pool)
	pipe = r.pipeline()

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='book')

	def callback(ch, method, properties, body):
		body = json.loads(body)
		title, i, downloads, word_dict = body

		print(" [x] Received %r" % i)

		# Persist
		for key in word_dict : pipe.rpush(key, json.dumps((title, i, downloads, word_dict[key])))
		pipe.execute()

		#element = r.lrange("that", 0, -1)

		# Clear db
		#for key in word_dict : r.delete(key) #delete entiere db

	channel.basic_consume(queue='book', on_message_callback=callback, auto_ack=True)

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
