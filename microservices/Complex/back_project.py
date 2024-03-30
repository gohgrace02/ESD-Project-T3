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
headers = { "Authorization": "Bearer sk_test_51O4n0jBWraf69XnWY4aVlVKRqQUCAFfd39aPqRYrDH1tVCUDkUv73npLZXUJcMEopBma6kK2JdyZEdh8aRCij6Lk00clrvlXD8" }

@app.route("/back_project/<int:project_id>", methods=['POST'])
def back_project(project_id):
    # get the data sent over from frontend
    # data includes project_id, backer_id ,pledge_amt, and card info for Stripe
    data = request.get_json()
    project_id = data['project_id']
    backer_id = data['backer_id']
    pledge_amt = data['pledge_amt']
    card = data['card']

    # create session
    # return create_session(backer_id)

# users will make a POST req to this when they click on the 'pledge' button
# this creates a checkout session and redirects the user to the stripe checkout url
@app.route("/create_checkout_session/<backer_id>", methods=['POST'])
def create_checkout_session(backer_id):
    data = request.get_json()
    project_id = data.get('project_id')
    pledge_amt = data.get('pledge_amt')
    price_id = data.get('price_id')
    quantity = data.get('quantity')
    cancel_url = data.get('cancel_url')
    success_url = "http://localhost:5173/success/?checkout_session_id={CHECKOUT_SESSION_ID}&return_url=" + cancel_url + "&project_id=" + project_id + "&pledge_amt=" + str(pledge_amt)
    params = {
        "success_url": success_url,
        "cancel_url": cancel_url,
        "mode": "payment",
        "payment_intent_data[capture_method]": "manual",
        "currency": "sgd",
        "customer": "cus_PooH6AYiaXWQLE", 
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": quantity,
    }
    response = requests.post('https://api.stripe.com/v1/checkout/sessions', params=params, headers=headers).json()
    # return redirect(response['url'])
    # return response['url']
    return response
    # return jsonify({'backer_id': backer_id})

# this function retrieves the checkout session
# then retrieves the setupintent id from that
# then the setupintent object
# then the payment method id from that



@app.route("/get_payment_intent_id/<checkout_session_id>", methods=['GET'])
def get_payment_intent_id(checkout_session_id):
    stripe_url = "https://api.stripe.com/v1/checkout/sessions/" + checkout_session_id
    try:
        response = requests.get(stripe_url,headers=headers).json()
        return response['payment_intent']
    except Exception as e:
        error_message = {
            "error_type": "payment_intent_id_retrieval_error",
            "error_message": str(e),
            "data": data
        }
        # print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        # channel.basic_publish(exchange=exchangename, routing_key="project.error",
        #     body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
        # print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the PaymentIntent ID from Stripe."
            }
        ), 500
        


# @app.route("/capture/<payment_intent_id>", methods=['POST'])



@app.route("/capture_all/<int:project_id>", methods=['POST', 'GET'])
# this collates all payment_intent_ids related to this given project_id and 
# captures all related payments
def capture_all(project_id):
    # get trackers by project_id
    url = "http://localhost:5001/project/" + str(project_id) + "/tracker"
    response = requests.get(url).json()
    tracker_list = response['data']['trackerList']
    # iterates through the list and calls capture_payment on each tracker
    for tracker in tracker_list:
        payment_intent_id = tracker['payment_intent_id']
        try:
            capture_payment(payment_intent_id)
        except Exception as e:
            error_message = {
                "error_type": "capture_all_error",
                "error_message": str(e),
                "data": data
            }
            # print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
            # channel.basic_publish(exchange=exchangename, routing_key="project.error",
            #     body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
            # print("\nProject error published to RabbitMQ Exchange.\n")
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred during capture_all() on back_project.py."
                }
            ), 500
    return jsonify({
        "code": 201,
        "status": "success"
    })



# this captures payment for only one payment_intent_id
def capture_payment(payment_intent_id):
    # data = request.get_json()
    # message = data.get('message')
    # # when goal has been reached right after a new tracker row is added
    # if message == "Project has been fulfilled":
    url = "https://api.stripe.com/v1/payment_intents/" + payment_intent_id + "/capture"
    try:
        response = requests.post(url, headers=headers).json()
        return response
    except Exception as e:
        error_message = {
            "error_type": "payment_capture_error",
            "error_message": str(e),
            "data": data
        }
        # print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        # channel.basic_publish(exchange=exchangename, routing_key="project.error",
        #     body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
        # print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred during payment capture on Stripe."
            }
        ), 500



if __name__ == '__main__':
    # connection = amqp_connection.create_connection() #get the connection to the broker
    # print("back_project: Connection established successfully")
    # channel = connection.channel()
    # receiveFulfilmentLog(channel)  # Start consuming messages from the queue
    app.run(host='0.0.0.0', port=5004, debug=True)