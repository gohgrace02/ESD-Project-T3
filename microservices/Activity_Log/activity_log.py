#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

import amqp_connection
import json
import pika
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/activity_log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

a_queue_name = environ.get('a_queue_name') or 'Activity_Log' # queue to be subscribed by Activity_Log microservice

db = SQLAlchemy(app)

CORS(app)

class Activity_Log(db.Model):
    __tablename__ = 'activity_log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer)
    data = db.Column(db.String(255))
    message = db.Column(db.String(255)) 
    microservice = db.Column(db.String(255))

    def __init__(self, code, data, message, microservice):
        self.code = code
        self.data = data
        self.message = message
        self.microservice = microservice
    
    def json(self):
        return {"log_id": self.log_id, 
                "code": self.code, 
                "data": self.data, 
                "message": self.message,
                "microservice": self.microservice
        }


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


def processLog(log):
    print("activity_log: Recording a log:")
    print(log)
    add_log(log)


def add_log(log):
    with app.app_context():

        new_log = Activity_Log(
            code=log['code'],
            data=str(log['data']),
            message=log['message'],
            microservice=log['microservice']
        )
        
        print("this is the activity log to be added: ")
        print(new_log) # prints some weird thing
        print(log) # prints some weird thing

        try:
            db.session.add(new_log)
            db.session.commit()
            print("created error log successfully.")
        except Exception as e:
            print("An error occurred while adding the error log. " + str(e))


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("activity_log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("activity_log: Connection established successfully")
    channel = connection.channel()
    receiveLog(channel)
    app.run(host='0.0.0.0', port=5002, debug=True)

# if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
#     print("This is flask for " + os.path.basename(__file__) + ": recording logs ...")
#     app.run(host='0.0.0.0', port=5002, debug=True)