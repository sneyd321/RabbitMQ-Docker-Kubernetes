import pika
import uuid, json

#Create connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#Create channel
channel = connection.channel()

#Declare exclusive queue to hold reply
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

#Initialize response
response = None
#Generate correlation id, this checks if the RPC call came from the correct spot
corr_id = str(uuid.uuid4())

#Callback for when service has completed the request
def on_response(ch, method, props, body):
    if corr_id == props.correlation_id:
        response = json.loads(body)
       
    
#Consume result in callback_queue
channel.basic_consume(queue=callback_queue,
                    on_message_callback=on_response,
                    auto_ack=True)




def send(data):
    channel.basic_publish(
        exchange='',
        routing_key='rpc_queue',
        properties=pika.BasicProperties(
            content_type="application/json",
            reply_to=callback_queue,
            correlation_id=corr_id,
        ),
        body=json.dumps(data))


send({"test": "hello"})
while response is None:
    connection.process_data_events()


