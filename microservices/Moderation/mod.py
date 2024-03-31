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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/mod'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/mod'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class Mod(db.Model):
#   __tablename__ = 'moderation'
#   moderationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#   comment = db.Column(db.Text, nullable=False)
#   actionTaken = db.Column(Enum('Approved', 'Rejected'), nullable=False)
#   reason = db.Column(db.Text, nullable=False)
#   moderatedAt = db.Column(db.TIMESTAMP)

#   def __init__(self, moderationID, comment, actionTaken, reason, moderatedAt):
#     self.moderationID = moderationID
#     self.comment = comment
#     self.actionTaken = actionTaken
#     self.reason = reason
#     self.moderatedAt = moderatedAt
      
#   def json(self):
#     return {
#         'moderationID': self.moderationID, 'comment': self.comment, 'actionTaken': self.actionTaken, 'reason': self.reason, 'moderatedAt': self.moderatedAt
#     }

# def is_vulgar():
#   # Probably need add more Vulgarities
#   url = "http://api1-ap.webpurify.com/services/rest//?method=webpurify.live.check&api_key=c4eb16473bd9be59faee65a329fdad48&text=fuck&format=json"

#   response = requests.get(url)

#   # Access the response content (replace with actual data parsing)
#   data = response.json()
#   # print(data)
#   if data["rsp"]["@attributes"]["stat"] == "fail":
#     print(data["rsp"]["err"]["@attributes"]["msg"]) 
#   elif data["rsp"]["found"] == 0:
#     return False
#   else:
#     return True

#   # return ["stupid", "bitch", "shit"]

@app.route("/project/<string:project_id>/moderate", methods=["POST"])
def moderate(project_id):
  # Checks if the feedback_info, rating and backerID key exists in the request body
  feedback_info = request.json.get("feedback_info")
  rating = request.json.get("rating")
  backer_id = request.json.get("backer_id")

  if not feedback_info:
    return jsonify(
        {
            "code": 400,
            "error": "Missing feedback_info in request body"
        }
    ), 400
  if not rating:
    return jsonify(
        {
            "code": 400,
            "error": "Missing rating in request body"
        }
    ), 400
  if not backer_id:
    return jsonify(
        {
            "code": 400,
            "error": "Missing backer_id in request body"
        }
    ), 400

  def check_vulgar(feedback_info):
    # Probably need add more Vulgarities
    url = f"http://api1-ap.webpurify.com/services/rest//?method=webpurify.live.check&api_key=07e7c189b92ff357331ffe3183a48578&text={feedback_info}&format=json"

    response = requests.get(url)
    
    # Access the response content (replace with actual data parsing)
    data = response.json()
    if data["rsp"]["found"] == "0":
      return False
    else:
      return True

  # Function returns true if vulgarity spotted and false if no vulgarities spotted
  is_vulgar = check_vulgar(feedback_info)

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
  if not is_vulgar:
    try:
      response = requests.post(url, json=moderation_data)
      print("Moderation result sent successfully.")
      return jsonify(
        {
            "code": 200,
            "moderation_status": "Approved, sent to feedback microservice"
        }
      ), 200 
    except requests.exceptions.RequestException as e:
      print(f"Error sending data to feedback microservice: {e}")
      return jsonify(
        {
            "code": 500,
            "moderation_status": "Approved, failed to send to feedback microservice"
        }
      ), 500 

  else:
    # Inform the error microservice
    #print('\n\n-----Invoking error microservice as order fails-----')
    print('\n\n-----Publishing the (order error) message with routing_key=mod.error-----')

    # invoke_http(error_URL, method="POST", json=order_result)
    channel.basic_publish(exchange=exchangename, routing_key="mod.error", 
        body=feedback_info, properties=pika.BasicProperties(delivery_mode = 2)) 
    # make message persistent within the matching queues until it is received by some receiver 
    # (the matching queues have to exist and be durable and bound to the exchange)

    # - reply from the invocation is not used;
    # continue even if this invocation fails        
    print("Please do not include profanities!")
    return jsonify(
        {
            "code": 500,
            "moderation_status": "Vulgarities found, do not include them"
        }
      ), 500 


if __name__ == "__main__":
  app.run(debug=True, port=5006, host="0.0.0.0")
