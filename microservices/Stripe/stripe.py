from flask import Flask, jsonify
from flask_cors import CORS
# import amqp_connection
import json

import requests

import stripe

app = Flask(__name__)
CORS(app)
app.config["STRIPE_SECRET_KEY"] = "sk_test_51O4n0jBWraf69XnWY4aVlVKRqQUCAFfd39aPqRYrDH1tVCUDkUv73npLZXUJcMEopBma6kK2JdyZEdh8aRCij6Lk00clrvlXD8"
stripe.api_key = app.config["STRIPE_SECRET_KEY"]
setup_intent_url = "/v1/setup_intents"

@app.route("/setup_intents", methods=['POST'])
def setup_intent():
    try:
        stripe.SetupIntent.create(payment_method_types=["card"])
        return josnify(
            {
                "client_secret": setup_intent.client_secret
            }
        ), 200
    except stripe.error.StripeError as e:
        return jsonify(
            {
                "error": str(e)
            }
        ), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)