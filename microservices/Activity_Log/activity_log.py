#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

#!/usr/bin/env python3
import amqp_connection
import json
import pika
from os import environ


a_queue_name = environ.get('a_queue_name') or 'Activity_Log' # queue to be subscribed by Activity_Log microservice


def receiveLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('activity_log: Consuming from queue:', a_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"activity_log: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("activity_log: Program interrupted by user.") 


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nactivity_log: Received an activity log by " + __file__)
    processLog(json.loads(body))
    print()

def processLog(order):
    print("activity_log: Recording an order log:")
    print(order)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("activity_log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("activity_log: Connection established successfully")
    channel = connection.channel()
    receiveLog(channel)

# if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
#     print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
#     app.run(host='0.0.0.0', port=5002, debug=True)