from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from os import environ
import re
import datetime
import requests


app = Flask(__name__)

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

@app.route("/moderate", methods=["POST"])
def moderate():
  # Checks if the feedback_info key exists in the request body
  comment = request.json.get("feedback_info")
  if not comment:
    return jsonify({"error": "Missing feedback_info in request body"}), 400

  # # instead of using get_json() to get the data from the request received, we use the above method of request.json.get
  # comment = request.get_json()
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

  # Function checks if the provided comment contains vulgar language.
  # def is_vulgar(comment):
  
  #   comment = comment.lower()
  #   comment = re.sub(r"[^\w\s]", "", comment)  # Removes punctuation
  #   vulgarity_list = load_vulgarity_list()
  
  #   for word in comment.split():
  #     if word in vulgarity_list:
  #       return True
  
  #   return False

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

  # Return moderation status to Project Microservice

  return jsonify({"moderation_status": "Rejected" if check_vulgar else "Approved"})

if __name__ == "__main__":
  app.run(debug=True)
