from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
import amqp_connection
import json
import pika

import os, sys

import requests

app = Flask(__name__)
CORS(app)

a_queue_name = 'Back_Project' # queue to be subscribed by Activity_Log microservice

project_URL = "http://localhost:5000/project"
tracker_URL = "http://localhost:5001/tracker"
activity_log_URL = "http://localhost:5002/activity_log"
error_URL = "http://localhost:5003/error"
# stripe_URL = ""


# this is to display the UI which shows the available projects
@app.route("/back_project")
def list_projects():
    response = requests.get(project_URL).json()
    projects = response['data']['projects']
    return render_template('list_projects.html', projects=projects)


@app.route("/back_project/<string:projectID>")
def project_details(projectID):
    response = requests.get(project_URL + '/' + projectID).json()
    project = response['data']
    return render_template('back_project.html', project=project)

# @app.route("/back_project/<string:projectID>")


def receiveFulfilmentLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('back_project: Consuming from queue:', a_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"back_project: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("back_project: Program interrupted by user.") 


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nback_project: Received a fulfilment log by " + __file__)
    processFulfilmentLog(json.loads(body))
    print()


def processFulfilmentLog(fulfilment):
    print("back_project: Recording a fulfilment log:")
    print(fulfilment)


if __name__ == '__main__':
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("back_project: Connection established successfully")
    channel = connection.channel()
    receiveFulfilmentLog(channel)  # Start consuming messages from the queue
    app.run(host='0.0.0.0', port=5004, debug=True)