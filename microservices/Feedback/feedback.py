from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    backer_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.TIMESTAMP)

    def __init__(self, backer_id, project_id, rating, comment, submitted_at):
        self.backer_id = backer_id
        self.project_id = project_id
        self.rating = rating
        self.comment = comment
        self.submitted_at = submitted_at
        
    def json(self):
        return {
            'feedback_id': self.feedback_id, 'backer_id': self.backer_id, 'project_id': self.project_id, 'rating': self.rating, 'comment': self.comment, 'submitted_at': self.submitted_at
        }
    
@app.route("/project/<string:project_id>/feedback", methods=['POST'])
def create_feedback(project_id):
    # need to check if feedback alr exists? (hvnt include code for this)

    data = request.get_json()
    feedback = Feedback(backer_id=data.get('backer_id'), project_id=project_id, rating=data.get('rating'), comment=data.get('comment'), submitted_at=data.get('submitted_at')) 

    try:
        db.session.add(feedback)
        db.session.commit()
        print("feedback added")
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "project_id": project_id
                },
                "message": "An error occurred creating the feedback."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": feedback.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)