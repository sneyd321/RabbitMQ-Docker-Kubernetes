import pika, json

#Create connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#Create channel
channel = connection.channel()
#Declare queue
channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    data = json.loads(body)
    print(data)
    data["test"] = "bye"
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=json.dumps(data))

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()