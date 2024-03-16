from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import os, sys

import requests

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

back_project_URL = "http://localhost:5004/back_project"
exchangename = "tracker" # exchange name
exchangetype = "direct" # use a 'direct' exchange to enable interaction

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # backer_id = db.Column(db.Integer, db.ForeignKey('backer.backer_id'))
    # project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    backer_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    pledge_amt = db.Column(db.Float)

    def __init__(self, backer_id, project_id, pledge_amt):
        self.backer_id = backer_id
        self.project_id = project_id
        self.pledge_amt = pledge_amt

    def json(self):
        return {"tracker_id": self.tracker_id, "backer_id": self.backer_id, "project_id": self.project_id, "pledge_amt": self.pledge_amt}


@app.route("/project/<int:project_id>/tracker", methods=['POST'])
def create_tracker(project_id):
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


@app.route("/project/<int:project_id>/test", methods=['POST'])
def test_tracker(project_id):
    # send a GET request to Project microservice, get the fundingGoal check whether the fundingGoal is reached

    project_fufilment(project_id)

    # Send a PUT request to Project microservice to update the goalReached status
    return "done"


# After updating Tracker database, check whether the goal of the project is reached - (GET funding_goal from Project for specific project_id)
# GET total amount from tracker for specific project_id (create this function in Tracker)
# IF the Project fundingGoal is reached:
# 1. Call the "project_fufilment" function
#    THEN The "project_fufilment" should send an event to backProject microservice
# 2. Send PUT request to project to update goalReached status (invoke method - wait for joycelyn's PUT Project function)
def project_fufilment(project_id):
    # Record project fulfilment event
    # print('\n\n-----Invoking back_project microservice-----')
    print('\n\n-----Publishing the (project fulfilment event) message with routing_key = fulfilment.info-----')  

    # need to include the project ID that has been fulfiled      
    message = {
        "project_id": project_id,
        "message": "Project has been fulfilled"
    }

    message_json = json.dumps(message)

    channel.basic_publish(exchange=exchangename, routing_key="fulfilment.info", 
        body=message_json, properties=pika.BasicProperties(delivery_mode = 2))
    
    print("\nFulfilment published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)