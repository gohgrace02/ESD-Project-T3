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
exchangename = "back_project_topic" # exchange name
exchangetype= "topic" # use a 'topic' exchange to enable interaction


# users will make a POST req to this when they click on the 'pledge' button
# this creates a checkout session and redirects the user to the stripe checkout url
@app.route("/create_checkout_session", methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    customer_id = data.get('customer_id')
    project_id = data.get('project_id')
    pledge_amt = data.get('pledge_amt')
    price_id = data.get('price_id')
    quantity = data.get('quantity')
    cancel_url = data.get('cancel_url')
    goal_reached = data.get('goal_reached')
    success_url = "http://localhost:5173/success/?checkout_session_id={CHECKOUT_SESSION_ID}&return_url=" + cancel_url + "&project_id=" + str(project_id) + "&pledge_amt=" + str(pledge_amt)
   
    # # creates delayed payment checkout session if goal not reached
    if not goal_reached:
        params = {
            "success_url": success_url,
            "cancel_url": cancel_url,
            "mode": "payment",
            "payment_intent_data[capture_method]": "manual", # delayed payment !
            "currency": "sgd",
            "customer": customer_id, 
            "line_items[0][price]": price_id,
            "line_items[0][quantity]": quantity,
        }
        response = requests.post('https://api.stripe.com/v1/checkout/sessions', params=params, headers=headers).json()
        return response
    
    # # creates immediate payment checkout session if goal reached
    else:
        params = {
            "success_url": success_url,
            "cancel_url": cancel_url,
            "mode": "payment",
            "payment_intent_data[capture_method]": "automatic", # immediate payment !
            "currency": "sgd",
            "customer": customer_id, 
            "line_items[0][price]": price_id,
            "line_items[0][quantity]": quantity,
        }
        response = requests.post('https://api.stripe.com/v1/checkout/sessions', params=params, headers=headers).json()
        return response



# this function retrieves the checkout session
# then retrieves the payment_intent_id from that
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
        print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        channel.basic_publish(exchange=exchangename, routing_key="project.error",
            body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
        print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred retrieving the PaymentIntent ID from Stripe."
            }
        ), 500
        



@app.route("/capture_all/<int:project_id>", methods=['POST', 'GET', 'PUT'])
# this collates all payment_intent_ids related to this given project_id and 
# captures all related payments
# called by POST request
def capture_all(project_id):
    # get trackers by project_id
    url = "http://localhost:5001/project/" + str(project_id) + "/tracker"
    # url = "http://tracker:5001/project/" + str(project_id) + "/tracker"
    response = requests.get(url).json()
    tracker_list = response['data']['trackerList']

    # iterates through the list and calls capture_payment on each tracker
    for tracker in tracker_list:
        if not tracker['captured']:
            payment_intent_id = tracker['payment_intent_id']
            try:
                capture_payment(payment_intent_id)
                tracker_id = tracker['tracker_id']

                response = requests.put("http://localhost:5001/tracker/" + str(tracker_id)).json()
                # response = requests.put("http://tracker:5001/tracker/" + str(tracker_id)).json()

                if response['code'] != 200:
                    # Handle tracker update error
                    return jsonify({"error": "Failed to update tracker data."}), 500
            except Exception as e:
                # Handle capture payment error
                return jsonify({"error": "An error occurred during payment capture."}), 500
    return jsonify({
        "code": 201,
        "status": "All payments captured and trackers updated successfully."
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
        print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        channel.basic_publish(exchange=exchangename, routing_key="project.error",
            body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
        print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred during payment capture on Stripe."
            }
        ), 500



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
    print("\nback_project: Received an backing creation log by " + __file__)
    processTrackerLog(json.loads(body))
    print()

def processTrackerLog(order):
    print("back_project: Recording an backing creation log:")
    print(order)



if __name__ == '__main__':
    # connection = amqp_connection.create_connection() #get the connection to the broker
    # print("back_project: Connection established successfully")
    # channel = connection.channel()
    # receiveFulfilmentLog(channel)  # Start consuming messages from the queue
    app.run(host='0.0.0.0', port=5004, debug=True)