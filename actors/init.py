import requests, pika, sys, os
from os import path

def main():

	def send(body):

		connection = pika.BlockingConnection(
		    pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()

		channel.queue_declare(queue='id')

		channel.basic_publish(exchange='', routing_key='id', body=body)

		print(" [x] Sent " + body)
		connection.close()
 
	# Send every IDs
	for i in range(40): send(str(i))

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)