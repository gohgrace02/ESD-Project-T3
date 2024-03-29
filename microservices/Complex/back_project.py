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
# creates line item based on pledge amount input
@app.route("/create_line_item/<backer_id>", methods=['POST'])
def create_line_item(backer_id):
    data = request.form['pledge_amt']
    

# this creates a checkout session and redirects the user to the stripe checkout url
@app.route("/create_checkout_session/<backer_id>", methods=['POST'])
def create_checkout_session(backer_id):
    params = {
        # "success_url": "http://localhost:5004/success/?session_id={CHECKOUT_SESSION_ID}",
        "success_url": "http://localhost:5004/success/{CHECKOUT_SESSION_ID}",
        "mode": "payment",
        "currency": "sgd",
        "customer": backer_id,
        "line_items[0][price]": "price_1OzXtuBWraf69XnWOJIEupXh",
        "line_items[0][quantity]": "1",
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
@app.route("/success/<session_id>", methods=['POST', 'GET'])
def get_payment_method_id(session_id):
    return session_id

if __name__ == '__main__':
    # connection = amqp_connection.create_connection() #get the connection to the broker
    # print("back_project: Connection established successfully")
    # channel = connection.channel()
    # receiveFulfilmentLog(channel)  # Start consuming messages from the queue
    app.run(host='0.0.0.0', port=5004, debug=True)