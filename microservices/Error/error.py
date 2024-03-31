#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

import amqp_connection
import json
import pika

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/error'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

e_queue_name = 'Error'        # queue to be subscribed by Error microservice

db = SQLAlchemy(app)

CORS(app)

class Error(db.Model):
    __tablename__ = 'error'
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


def receiveError(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)
        print('error microservice: Consuming from queue:', e_queue_name)
        channel.start_consuming() # an implicit loop waiting to receive messages; 
        #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"error microservice: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("error microservice: Program interrupted by user.")


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nerror microservice: Received an error by " + __file__)
    processError(body)
    print()


def processError(errorMsg):
    print("error microservice: Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
        add_log(error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()


def add_log(error):
    with app.app_context():

        new_log = Error(
            code=error['code'],
            data=str(error['data']),
            message=error['message'],
            microservice=error['microservice']
        )
        
        print("this is the error log to be added: ")
        print(new_log) # prints some weird thing
        print(error) # prints some weird thing

        try:
            db.session.add(new_log)
            db.session.commit()
            print("created error log successfully.")
        except Exception as e:
            print("An error occurred while adding the error log. " + str(e))


if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    print("error microservice: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("error microservice: Connection established successfully")
    channel = connection.channel()
    receiveError(channel)
    app.run(host='0.0.0.0', port=5003, debug=True)