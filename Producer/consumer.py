import pika 

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='lease', durable=True)
channel.exchange_declare(exchange='lease-direct', durable=True, auto_delete=True)
channel.queue_bind(queue="lease", exchange='lease-direct', routing_key="lease")

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue='lease', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()