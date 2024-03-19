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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Mod(db.Model):
  __tablename__ = 'moderation'
  moderationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  comment = db.Column(db.Text, nullable=False)
  actionTaken = db.Column(Enum('Approved', 'Rejected'), nullable=False)
  reason = db.Column(db.Text, nullable=False)
  moderatedAt = db.Column(db.TIMESTAMP)

  def __init__(self, moderationID, comment, actionTaken, reason, moderatedAt):
    self.moderationID = moderationID
    self.comment = comment
    self.actionTaken = actionTaken
    self.reason = reason
    self.moderatedAt = moderatedAt
      
  def json(self):
    return {
        'moderationID': self.moderationID, 'comment': self.comment, 'actionTaken': self.actionTaken, 'reason': self.reason, 'moderatedAt': self.moderatedAt
    }

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
  comment = request.json.get("feedback_info")
  rating = request.json.get("rating")
  backerID = request.json.get("backerID")

  if not comment:
    return jsonify({"error": "Missing feedback_info in request body"}), 400
  if not rating:
    return jsonify({"error": "Missing rating in request body"}), 400
  if not backerID:
    return jsonify({"error": "Missing backerID in request body"}), 400

  def is_vulgar(comment):
    # Probably need add more Vulgarities
    url = f"http://api1-ap.webpurify.com/services/rest//?method=webpurify.live.check&api_key=c4eb16473bd9be59faee65a329fdad48&text={comment}&format=json"

    response = requests.get(url)
    

    # Access the response content (replace with actual data parsing)
    data = response.json()
    # print(data)
    # if data["rsp"]["@attributes"]["stat"] == "fail":
    #   print(data["rsp"]["err"]["@attributes"]["msg"])
    if data["rsp"]["found"] == "0":
      return False
    else:
      return True

  # Function returns true if vulgarity spotted and false if no vulgarities spotted
  check_vulgar = is_vulgar(comment)

  # # Send the feedback to Feedback Microservice based on moderation result
  # # (Replace this with your actual implementation for sending the feedback)
  # if not is_vulgar:
  #   # Send to Feedback Microservice (success scenario)
  #   print(f"Feedback is not vulgar: {comment}")
  # else:
  #   # Send to Error Microservice (rejected scenario)
  #   print(f"Feedback contains vulgarity: {comment}")

  # DATA FOR DATABASE
  moderationID = 000 #example
  actionTaken = "Rejected" if is_vulgar else "Approved"
  reason = "NIL" if not is_vulgar else "Vulgarity Spotted"
  moderatedAt = datetime.datetime.now()

  # Checking if ^ is proeprly constructed
  # return jsonify({"moderationID": moderationID,
  #                 "comment": comment,
  #                 "actionTaken":  actionTaken,
  #                 "reason": reason, 
  #                 "moderatedAt": moderatedAt
  #               })


  
  my_url = f"http://127.0.0.1:5000/project/{project_id}/feedback"
  # response = requests.post(my_url, json=moderation_status)

  # try:
  #   response = requests.post(my_url, json=moderation_status)
  #   response.raise_for_status()  # Raise an exception for non-2xx status codes
  #   print("Moderation result sent successfully.")

  # except requests.exceptions.RequestException as e:
  #   print(f"Error sending data to feedback microservice: {e}")


  # Replace with the actual base URL of your application where the feedback microservice is running
  base_url = "http://127.0.0.1:5007"

  # Project ID (replace with the actual value)
  project_id = "1234"

  # Data to be sent (replace with actual content from your moderation process)
  moderation_data = {
      "backerID": backerID,
      "rating": rating,
      "comment": comment,
      "submittedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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

    # invoke_http(error_URL, method="POST", json=order_result)
    channel.basic_publish(exchange=exchangename, routing_key="mod.error", 
        body=comment, properties=pika.BasicProperties(delivery_mode = 2)) 
    # make message persistent within the matching queues until it is received by some receiver 
    # (the matching queues have to exist and be durable and bound to the exchange)

    # - reply from the invocation is not used;
    # continue even if this invocation fails        
    print("Please do not include profanities!")


  return jsonify({"moderation_status": "Rejected, feedback not posted" if check_vulgar else "Approved"})

if __name__ == "__main__":
  app.run(debug=True, port=5006, host="0.0.0.0")
