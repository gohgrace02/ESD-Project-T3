from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from os import environ
from flask_cors import CORS
import sys
import re
import datetime
import requests

import pika
import json
import amqp_connection



app = Flask(__name__)
CORS(app)

exchangename = "mod_topic" # exchange name
exchangetype="topic" # use a 'topic' exchange to enable interaction

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/mod'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/mod'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/project/<string:project_id>/moderate", methods=["POST"])
def moderate(project_id):
  # Checks if the feedback_info, rating and backerID key exists in the request body
  feedback_info = request.json.get("feedback_info")
  rating = request.json.get("rating")
  backer_id = request.json.get("backer_id")

  if not feedback_info:
    return jsonify({"error": "Missing feedback_info in request body"}), 400
  if not rating:
    return jsonify({"error": "Missing rating in request body"}), 400
  if not backer_id:
    return jsonify({"error": "Missing backer_id in request body"}), 400

  def is_vulgar(feedback_info):
    # Probably need add more Vulgarities
    url = f"http://api1-ap.webpurify.com/services/rest//?method=webpurify.live.check&api_key=07e7c189b92ff357331ffe3183a48578&text={feedback_info}&format=json"

    response = requests.get(url)
    

    # Access the response content (replace with actual data parsing)
    data = response.json()
    # print(data)
    if data["rsp"]["found"] == "0":
      return False
    else:
      return True

  # Function returns true if vulgarity spotted and false if no vulgarities spotted
  check_vulgar = is_vulgar(feedback_info)

  my_url = f"http://feedback:5007/project/{project_id}/feedback"

  # Replace with the actual base URL of your application where the feedback microservice is running
  # base_url = "http://127.0.0.1:5007"
  base_url = "http://feedback:5007"

  # Data to be sent (replace with actual content from your moderation process)
  moderation_data = {
      "backer_id": backer_id,
      "rating": rating,
      "feedback_info": feedback_info,
      "submitted_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  }

  # Construct the complete URL
  url = f"{base_url}/project/{project_id}/feedback"

  # Send the POST request with JSON data
  if not check_vulgar:
    try:
      response = requests.post(url, json=moderation_data)
      print("Moderation result sent successfully.")

    except requests.exceptions.RequestException as e:
      print(f"Error sending data to feedback microservice: {e}")

  else:
    # Inform the error microservice
    #print('\n\n-----Invoking error microservice as order fails-----')
    print('\n\n-----Publishing the (order error) message with routing_key=mod.error-----')

    message = {
        "code": 400,
        "data": feedback_info,
        "message": "Moderation is unsuccessful. Feedback not posted.",
        "microservice": "moderation"
    }

    # invoke_http(error_URL, method="POST", json=order_result)
    channel.basic_publish(exchange=exchangename, routing_key="mod.error", 
        body=json.dumps(message), properties=pika.BasicProperties(delivery_mode = 2)) 
    # make message persistent within the matching queues until it is received by some receiver 
    # (the matching queues have to exist and be durable and bound to the exchange)

    # - reply from the invocation is not used;
    # continue even if this invocation fails        
    print("Please do not include profanities!")


  return jsonify({"moderation_status": "Rejected, feedback not posted" if check_vulgar else "Approved"})

if __name__ == "__main__":
  app.run(debug=True, port=5006, host="0.0.0.0")
