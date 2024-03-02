from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from os import environ
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Mod(db.Model):
  __tablename__ = 'moderation'
  moderationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  feedbackID = db.Column(db.Integer)
  moderatorID = db.Column(db.Integer)
  actionTaken = db.Column(Enum('Pending', 'Approved', 'Rejected'), nullable=False)
  reason = db.Column(db.Text, nullable=False)
  moderatedAt = db.Column(db.TIMESTAMP)

  def __init__(self, moderationID, feedbackID, moderatorID, actionTaken, reason, moderatedAt):
    self.moderationID = moderationID
    self.feedbackID = feedbackID
    self.moderatorID = moderatorID
    self.actionTaken = actionTaken
    self.reason = reason
    self.moderatedAt = moderatedAt
      
  def json(self):
    return {
        'moderationID': self.moderationID, 'feedbackID': self.feedbackID, 'moderatorID': self.moderatorID, 'actionTaken': self.actionTaken, 'reason': self.reason, 'moderatedAt': self.moderatedAt
    }

def load_vulgarity_list():
  # Probably need add more Vulgarities
  return ["stupid", "bitch", "cock"]

def is_vulgar(text):
  """Checks if the provided text contains vulgar language.

  Args:
      text: The text to check for vulgarity.

  Returns:
      True if the text contains vulgar language, False otherwise.
  """
  text = text.lower()
  text = re.sub(r"[^\w\s]", "", text)  # Removes punctuation
  vulgarity_list = load_vulgarity_list()

  for word in text.split():
    if word in vulgarity_list:
      return True

  return False

@app.route("/check_vulgarity", methods=["POST"])
## Should delete Feedback but not sure how :/
def check_vulgarity():
  text = request.json.get("text")
  if not text:
      return jsonify({"error": "Missing text data in request body"}), 400

  if is_vulgar(text):
    return jsonify({"vulgar": True})
  else:
    return jsonify({"vulgar": False})

if __name__ == "__main__":
  app.run(debug=True)
