from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import amqp_connection
import json
import pika

import os, sys

import requests

app = Flask(__name__)
CORS(app)

a_queue_name = 'Back_Project' # queue to be subscribed by Activity_Log microservice

@app.route("/back_project/<int:project_id>", methods=['POST'])
def back_project(project_id):
    # get the data sent over from frontend
    # data includes project_id, backer_id ,pledge_amt, and card info for Stripe
    data = request.get_json()
    project_id = str(project_id)
    backer_id = data.get("backer_id")
    pledge_amt = data.get("pledge_amt")

    # sends card info to Stripe
    card_info = data.get("card_info")
    # receives success/failure status from Stripe
    stripe_status = True


    # sends project_id, backer_id, pledge_amt to tracker.py
    if stripe_status:
        tracker_data = {
            "project_id": project_id,
            "backer_id": backer_id,
            "pledge_amt": pledge_amt
        }
        tracker_URL = "http://localhost:5001/project"
        response = requests.post(tracker_URL + '/' + project_id + '/tracker', json=tracker_data)
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": "Failed to update project data"}), response.status_code

    # receives tracker status from tracker.py

    # sends pledge_amt and tracker status to frontend

    # activity_log via amqp

    # error via amqp


def receiveFulfilmentLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('back_project: Consuming from queue:', a_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
#     except pika.exceptions.AMQPError as e:
#         print(f"back_project: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

#     except KeyboardInterrupt:
#         print("back_project: Program interrupted by user.") 


# def callback(channel, method, properties, body): # required signature for the callback; no return
#     print("\nback_project: Received a fulfilment log by " + __file__)
#     processFulfilmentLog(json.loads(body))
#     print()


# def processFulfilmentLog(fulfilment):
#     print("back_project: Recording a fulfilment log:")
#     print(fulfilment)


if __name__ == '__main__':
    # connection = amqp_connection.create_connection() #get the connection to the broker
    # print("back_project: Connection established successfully")
    # channel = connection.channel()
    # receiveFulfilmentLog(channel)  # Start consuming messages from the queue
    app.run(host='0.0.0.0', port=5004, debug=True)