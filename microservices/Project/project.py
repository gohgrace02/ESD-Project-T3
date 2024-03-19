from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

from datetime import datetime

import sys
import pika
import json
import amqp_connection

exchangename = "project_topic" # exchange name
exchangetype = "topic" # use a 'direct' exchange to enable interaction

# #create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

# #if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/project'
# idk why it doesnt work if I use the above --> need to use command prompt for the above to work 
# use: set dbURL=mysql+mysqlconnector://root@localhost:3306/project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)  

class Project(db.Model):
    __tablename__ = 'project'

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)  # You can adjust the length as needed
    description = db.Column(db.Text, nullable=True)   # Assuming description can be nullable
    creator_id = db.Column(db.String(255), nullable=False)  # Adjust length as needed
    funding_goal = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(255), nullable=False)  
    goal_reached = db.Column(db.Boolean, nullable=False, default=False) # Default to False, as boolean.


    def __init__(self, project_id, name, description, creator_id, funding_goal, deadline, creation_time, status, goal_reached):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.funding_goal = funding_goal
        self.deadline = deadline
        self.creation_time = creation_time
        self.status = status
        self.goal_reached = goal_reached


    def json(self):
        return {"project_id": self.project_id, 
                "name": self.name, 
                "description": self.description, 
                "creator_id": self.creator_id, 
                "funding_goal": self.funding_goal, 
                "deadline": self.deadline, 
                "creation_time": self.creation_time, 
                "status": self.status, 
                "goal_reached": self.goal_reached}

@app.route("/project")
def get_all():
    projectlist = db.session.scalars(db.select(Project)).all()


    if len(projectlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "projects": [project.json() for project in projectlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no projects."
        }
    ), 404


@app.route("/project/<int:project_id>")
def find_by_projectid(project_id):
    project = db.session.scalars(
    	db.select(Project).filter_by(project_id=project_id).
    	limit(1)
).first()


    if project:
        return jsonify(
            {
                "code": 200,
                "data": project.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Project not found."
        }
    ), 404


@app.route("/project", methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(project_id = data.get('project_id'), name = data.get('name'), description = data.get('description'), creator_id = data.get('creator_id'), funding_goal = data.get('funding_goal'), deadline = data.get('deadline'), creation_time = data.get('creation_time'), status = data.get('status'), goal_reached = data.get('goal_reached'))

    try:
        db.session.add(project)
        db.session.commit()
    except Exception as e:
        error_message = {
            "error_type": "create_project_error",
            "error_message": str(e),
            "data": data
        }
        print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        channel.basic_publish(exchange=exchangename, routing_key="project.error", 
            body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2)) 
        print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the project."
            }
        ), 500
    
    print('\n\n-----Publishing the (project info) message with routing_key=project.info-----')
    channel.basic_publish(exchange=exchangename, routing_key="project.info", 
        body=json.dumps(data), properties=pika.BasicProperties(delivery_mode = 2)) 
    print("\nProject info published to RabbitMQ Exchange.\n")
    return jsonify(
        {
            "code": 201,
            "data": project.json()
        }
    ), 201

@app.route("/project/<int:project_id>", methods=['PUT'])
def update_project(project_id):
    project = db.session.scalars(db.select(Project).filter_by(project_id=project_id).limit(1)).first()
    if project:
        data = request.get_json()
        if data['goal_reached']:
            project.goal_reached = data['goal_reached']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": project.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "project_id": project_id
            },
            "message": "Project not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)