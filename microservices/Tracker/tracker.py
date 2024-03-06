from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    trackerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # backerID = db.Column(db.Integer, db.ForeignKey('backer.backerID'))
    # projectID = db.Column(db.Integer, db.ForeignKey('project.projectID'))
    backerID = db.Column(db.Integer)
    projectID = db.Column(db.Integer)
    pledgeAmt = db.Column(db.Float)

    def __init__(self, backer_id, project_id, pledge_amt):
        self.backerID = backer_id
        self.projectID = project_id
        self.pledgeAmt = pledge_amt

    def json(self):
        return {"trackerID": self.trackerID, "backerID": self.backerID, "projectID": self.projectID, "pledgeAmt": self.pledgeAmt}


@app.route("/project/<int:project_id>/tracker", methods=['POST'])
def create_tracker(project_id):
    # To extract backerID from the user session
    # backerID = session.get('backerID')
    
    # To extract pledgeAmt from the request payload
    data = request.get_json()
    pledge_amt = data.get('pledgeAmt')

    # Create a new Tracker object
    tracker = Tracker(6, project_id, pledge_amt)

    try:
        db.session.add(tracker)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "ProjectID": project_id
                },
                "message": "An error occurred creating the tracker."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": tracker.json()
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)