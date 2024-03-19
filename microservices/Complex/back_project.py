from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import json

import os, sys

import requests

app = Flask(__name__)
CORS(app)


@app.route("/back_project/<string:project_id>", methods=['POST'])
def back_project(project_id):
    # get the data sent over from frontend
    # data includes project_id, backer_id ,pledge_amt, and card info for Stripe
    data = request.get_json()
    backer_id = data.get("backer_id")
    pledge_amt = data.get("pledge_amt")
    card_info = data.get("card_info")
    

    # sends card info to Stripe
    # receives success/failure status from Stripe
    stripe_status = True


    # sends project_id, backer_id, pledge_amt to tracker.py
    if stripe_status:
        tracker_data = {
            "backer_id": backer_id,
            "pledge_amt": pledge_amt
        }
        tracker_URL = "http://localhost:5001/project"
        response = requests.post(tracker_URL + '/' + str(project_id) + '/tracker', json=tracker_data).json()
        return response
    # receives tracker status from tracker.py

    # sends pledge_amt and tracker status to frontend

    # activity_log via amqp

    # error via amqp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

