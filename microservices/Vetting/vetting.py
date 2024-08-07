from flask import Flask, request, jsonify
from requests import post
from flask_cors import CORS
from textblob import TextBlob

import sys
import pika
import json
import amqp_connection

exchangename = "vetting_topic" # exchange name
exchangetype = "topic" # use a 'direct' exchange to enable interaction

# #create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

# #if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

app = Flask(__name__)
CORS(app)  

PROJECT_MICROSERVICE_URL = "http://project:5000/project"
# PROJECT_MICROSERVICE_URL = "http://localhost:5000/project"

def vet_project(project_data):
    # Add your vetting criteria here
    if 'name' not in project_data: #checking works
        return False
    
    # Perform sentiment analysis on the project description
    description = project_data.get('description', '')
    blob = TextBlob(description)
    sentiment_score = blob.sentiment.polarity

    # Reject projects with negative sentiment
    if sentiment_score < 0:
        return False

    return True

@app.route("/vetting", methods=['POST'])
def vetting_endpoint():

    data = request.get_json()

    if vet_project(data):
        # If vetting is approved, post the project to the project microservice
        response = post(PROJECT_MICROSERVICE_URL, json=data)

        if response.status_code == 201:
            message = {
                "code": 201,
                "data": str(data),
                "message": "Vetting successful. Project is created successfully.",
                "microservice": "vetting"
            }
            print("Data received:", message)
            print('\n\n-----Publishing the (vetting info) message with routing_key=vetting.info-----')
            channel.basic_publish(exchange=exchangename, routing_key="vetting.info", 
                body=json.dumps(message), properties=pika.BasicProperties(delivery_mode = 2)) 
            print("\nVetting info published to RabbitMQ Exchange.\n")

            return jsonify({
                "code": 201,
                "data": str(data),
                "message": "Vetting successful. Project is created successfully.",
                "microservice": "vetting"
                }), 201
        else:
            message = {
                "code": response.status_code,
                "data": str(data),
                "message": "Vetting successful. Error creating project.",
                "microservice": "vetting"
            }            
            print('\n\n-----Publishing the (vetting error) message with routing_key=vetting.error-----')
            channel.basic_publish(exchange=exchangename, routing_key="vetting.error", 
                body=json.dumps(message), properties=pika.BasicProperties(delivery_mode = 2)) 
            print("\nVetting error published to RabbitMQ Exchange.\n")
            return jsonify({
                "code": response.status_code,
                "data": str(data),
                "message": "Vetting successful. Error creating project.",
                "microservice": "vetting"
                })
    else:
        message = {
            "code": 400,
            "data": str(data),
            "message": "Vetting is unsuccessful. Project not created.",
            "microservice": "vetting"
        }
        print('\n\n-----Publishing the (vetting error) message with routing_key=vetting.error-----')
        channel.basic_publish(exchange=exchangename, routing_key="vetting.error", 
            body=json.dumps(message), properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nVetting error published to RabbitMQ Exchange.\n")
        return jsonify({
            "code": 400,
            "data": str(data),
            "message": "Vetting is unsuccessful. Project not created.",
            "microservice": "vetting"
            }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)