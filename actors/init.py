import requests, pika, sys, os
from os import path

# def filterAndSave(start, end):
# 	l = [requests.get("https://gutendex.com/books/" + str(i)) for i in range(start, end)]
# 	l = [e for e in l if e.status_code == 200]

# 	f = open("ids.txt", "w")

# 	for i in range(len(l)) : f.write(str(i+1) + "\n")

# 	f.close()

def main():

	# if not(path.exists("ids.txt")) : 
	# 	print("LOADING : scraping good IDs")
	# 	filterAndSave(1, 30) # About 5 mins : 2000
	# 	print("LOADING : Finish")

	# f = open("ids.txt", "r")

	# ids = [e[:-1] for e in f.readlines()]

	def send(body):

		connection = pika.BlockingConnection(
		    pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()

		channel.queue_declare(queue='id')

		channel.basic_publish(exchange='', routing_key='id', body=body)

		print(" [x] Sent " + body)
		connection.close()

	# Send every good IDs
	# for e in ids : send(e)
 
	# Send every IDs
	for i in range(200): send(str(i))

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)