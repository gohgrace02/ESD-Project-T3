from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from flask_cors import CORS

import os, sys
from dotenv import load_dotenv
load_dotenv()

import requests

import pika
import json
import amqp_connection

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
headers = { "Authorization": "Bearer " + os.getenv("STRIPE_PUB_KEY") }


# back_project_URL = "http://localhost:5004/back_project"
# back_project_URL = "http://back_project:5004/back_project"
exchangename = "tracker" # exchange name
exchangetype = "direct" # use a 'direct' exchange to enable interaction

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

db = SQLAlchemy(app)

CORS(app)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # backer_id = db.Column(db.Integer, db.ForeignKey('backer.backer_id'))
    # project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    backer_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    pledge_amt = db.Column(db.Float)
    pledge_amt = db.Column(db.Float)
    payment_intent_id = db.Column(db.String(255))
    captured = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, backer_id, project_id, pledge_amt, payment_intent_id, captured):
        self.backer_id = backer_id
        self.project_id = project_id
        self.pledge_amt = pledge_amt
        self.payment_intent_id = payment_intent_id
        self.captured = captured

    def json(self):
        return {"tracker_id": self.tracker_id, 
                "backer_id": self.backer_id, 
                "project_id": self.project_id, 
                "pledge_amt": self.pledge_amt,
                "payment_intent_id": self.payment_intent_id,
                "captured": self.captured
        }


@app.route("/project/<int:project_id>/tracker")
def get_all(project_id):
    # Filter tracker data based on the specified project_id
    trackerList = Tracker.query.filter_by(project_id=project_id).all()

    if trackerList:
        # Convert tracker objects to JSON format
        tracker_json = [tracker.json() for tracker in trackerList]
        return jsonify({
            "code": 200,
            "data": {
                "trackerList": tracker_json
            }
        }), 200
    else:
        return jsonify({
            "code": 404,
            "message": "There are no trackers for the specified project ID."
        }), 404


# Previous function used to update tracker database
@app.route("/project/<int:project_id>/test", methods=['POST'])
def test_tracker(project_id):
    # To extract backer_id from the user session
    # backer_id = session.get('backer_id')
    
    # To extract pledge_amt from the request payload
    data = request.get_json()
    pledge_amt = data.get('pledge_amt')

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
                    "project_id": project_id
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


# create_tracker function:
# 1. Update Tracker DB when backer backs a project 
# 2. IF funding_goal is reached will sent an event to back_project microservice and update goal_reached from Project DB
@app.route("/project/<int:project_id>/tracker", methods=['POST'])
def create_tracker(project_id):
    # TO DO: extract backer_id from the user session
    
    # Extract pledge_amt from the request payload
    data = request.get_json()
    pledge_amt = data.get('pledge_amt')
    backer_id = data.get('backer_id')
    payment_intent_id = data.get('payment_intent_id')
    # check goal_reached status of project
    url = "http://localhost:5000/project/" + str(project_id)
    goal_reached = requests.get(url).json()['data']['goal_reached']

    # 'captured' value is set to False if goal not reached
    if not goal_reached:
        captured = False
    else:
        captured = True

    # Create a new Tracker object, for now the backer_id is hardcoded
    tracker = Tracker(backer_id, project_id, pledge_amt, payment_intent_id, captured)

    try:
        db.session.add(tracker)
        db.session.commit()
        # return json of tracker
        # return jsonify(
        #     {
        #         "code": 201,
        #         "data": tracker.json()
        #     }
        # ), 201
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "project_id": project_id
                },
                "message": "An error occurred creating the tracker."
            }
        ), 500
    


    # Send a GET request to Project microservice to get the funding_goal
    project_URL = "http://localhost:5000/project"
    # project_URL = "http://project:5000/project"
    response = requests.get(project_URL + '/' + str(project_id)).json()
    data = response['data']
    funding_goal = response['data']['funding_goal']

    print(data)
    print(funding_goal)
    print(check_funding_goal(project_id, funding_goal))

    # Check whether the funding_goal is reached
    if(check_funding_goal(project_id, funding_goal)):
        print("funding goal is met! Project fufilment message will be sent to back_project and goal_reached will be updated")
        # Send an event to backProject microservice
        payment_capture_status = project_fufilment(project_id, payment_intent_id)

        # Send a PUT request to Project microservice to update the goalReached status
        new_data = {
            "goal_reached": 1
        }
        response = requests.put(project_URL + '/' + str(project_id), json=new_data)
        
        if response.status_code == 200:
            return jsonify(
                {
                    "payment_capture_status": payment_capture_status['status'],
                    "tracker_status": "Tracker created and Project data updated successfully"
                }
            ), 200
        else:
            return jsonify(
                {
                    "error": "Failed to update project data"
                }
            ), response.status_code
    
    return "Funding Goal has not been reached"


# check_funding_goal returns "True" if funding_goal is met else returns "False"
def check_funding_goal(project_id, funding_goal):
    # Query the Tracker table to get the sum of pledge_amt for the given project_id
    pledge_sum = db.session.query(func.sum(Tracker.pledge_amt)).filter(Tracker.project_id == project_id).scalar()
    
    # Check if the funding goal is met
    if pledge_sum is not None and pledge_sum >= funding_goal:
        funding_goal_met = True
    else:
        funding_goal_met = False

    return funding_goal_met


# project_fufilment sends fulfilment message to back_project
def project_fufilment(project_id):
    # Record project fulfilment event
    # print('\n\n-----Invoking back_project microservice-----')
    print('\n\n-----Publishing the (project fulfilment event) message with routing_key = fulfilment.info-----')  

    # need to include the project ID that has been fulfiled      
    json = {
        "project_id": project_id,
        "message": "Project has been fulfilled"
    }
    url = "http://localhost:5004/capture_all/" + str(project_id)
    try:
        response = requests.post(url, json=json).json()
        return jsonify({
            "code": 201,
            "status": response['status']
        })
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "project_id": project_id,
                    "message": "An error occurred while capturing payments for this project on Stripe."
                },
            }
        ), 500
    # message_json = json.dumps(message)

    # channel.basic_publish(exchange=exchangename, routing_key="fulfilment.info", 
    #     body=message_json, properties=pika.BasicProperties(delivery_mode = 2))
    
    # print("\nFulfilment published to RabbitMQ Exchange.\n")
    # # - reply from the invocation is not used;
    # # continue even if this invocation fails


# update tracker "captured" value
@app.route("/tracker/<int:tracker_id>", methods=['PUT'])
def update_tracker(tracker_id):
    tracker = db.session.scalars(db.select(Tracker).filter_by(tracker_id=tracker_id)).first()
    if tracker:
        if not tracker.captured:
            tracker.captured = True
            try:
                db.session.commit()
                return jsonify(
                    {
                        "code": 200,
                        "data": tracker.json()
                    }
                )
            except Exception as e:
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "tracker_id": tracker_id
                        },
                        "message": "Tracker not found."
                    }
                ), 404
        else:
            return jsonify({"message": "Tracker already captured.", "code": 200}), 200
    else:
        # Tracker not found
        return jsonify({"message": "Tracker not found.", "code": 404}), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)