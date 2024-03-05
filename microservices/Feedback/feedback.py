from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum  #for status enum
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedbackID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    backerID = db.Column(db.Integer)
    projectID = db.Column(db.Integer)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    submittedAt = db.Column(db.TIMESTAMP)
    status = db.Column(Enum('Pending', 'Approved', 'Rejected'), nullable=False)

    def __init__(self, backerID, projectID, rating, comment, submittedAt, status):
        self.backerID = backerID
        self.projectID = projectID
        self.rating = rating
        self.comment = comment
        self.submittedAt = submittedAt
        self.status = status
        
    def json(self):
        return {
            'feedbackID': self.feedbackID, 'backerID': self.backerID, 'projectID': self.projectID, 'rating': self.rating, 'comment': self.comment, 'submittedAt': self.submittedAt, 'status': self.status
        }
    
@app.route("/project/<int:project_id>/feedback", methods=['POST'])
def create_feedback(projectId):
    # need to check if feedback alr exists? (hvnt include code for this)

    data = request.get_json()
    feedback = Feedback(projectId, **data) #KIV

    try:
        db.session.add(feedback)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "ProjectID": projectId
                },
                "message": "An error occurred creating the feedbacl."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": feedback.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)