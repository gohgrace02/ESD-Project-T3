from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer)
    rating = db.Column(db.Integer, nullable=False)
    feedback_info = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.TIMESTAMP)

    def __init__(self, user_id, name, project_id, rating, feedback_info, submitted_at):
        self.user_id = user_id
        self.name = name
        self.project_id = project_id
        self.rating = rating
        self.feedback_info = feedback_info
        self.submitted_at = submitted_at
        
    def json(self):
        return {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'name': self.name,
            'project_id': self.project_id,
            'rating': self.rating,
            'feedback_info': self.feedback_info,
            'submitted_at': self.submitted_at
        }

@app.route("/get_feedback/<int:project_id>/", methods=['GET'])
def get_feedback(project_id):
    feedback_list = db.session.scalars(
        db.select(Feedback).filter_by(project_id=project_id)
    )
    if feedback_list:
        return jsonify(
            {
                "code": 200,
                "feedback_list": [feedback.json() for feedback in feedback_list]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No feedbacks for this project."
        }
    ), 404



@app.route("/create_feedback/<int:project_id>/", methods=['POST'])
def create_feedback(project_id):
    # need to check if feedback alr exists? (hvnt include code for this)

    data = request.get_json()
    feedback = Feedback(user_id=data.get('user_id'),
                        name=data.get('name'),
                        project_id=project_id,
                        rating=data.get('rating'),
                        feedback_info=data.get('feedback_info'),
                        submitted_at=data.get('submitted_at')
                ) 
    print(data)

    try:
        db.session.add(feedback)
        db.session.commit()
        print("feedback added")
    except Exception as e:
        print("An error occurred:", str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the feedback: " + str(e)
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": feedback.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)