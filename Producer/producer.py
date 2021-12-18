import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='lease', durable=True)
exchange = channel.exchange_declare(exchange='lease-direct', durable=True, auto_delete=True)
channel.queue_bind(queue="lease", exchange='lease-direct', routing_key="lease")



channel.basic_publish(exchange='lease-direct', routing_key='lease', body=json.dumps(create_lease()))
connection.close()
