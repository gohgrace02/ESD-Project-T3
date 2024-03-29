from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS


from datetime import datetime


import sys
import pika
import json
import amqp_connection


exchangename = "pledge_options_topic" # exchange name
exchangetype = "topic" # use a 'direct' exchange to enable interaction


# #create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection()
channel = connection.channel()


# #if the exchange is not yet created, exit the program
if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/project'
# idk why it doesnt work if I use the above --> need to use command prompt for the above to work 
# use: set dbURL=mysql+mysqlconnector://root@localhost:3306/project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)  

# CREATE TABLE IF NOT EXISTS `pledge_options` (
#     `option_id` INT AUTO_INCREMENT,
#     `title` VARCHAR(255) NOT NULL,
#     `description` TEXT,
#     `creator_id` VARCHAR(255) NOT NULL,
#     `project_id` INT NOT NULL,
#     `pledge_amt` INT NOT NULL,
#     `price_id` VARCHAR(255) NOT NULL,
#   PRIMARY KEY (`option_id`)

class Pledge_option(db.Model):
    __tablename__ = 'pledge_options'


    option_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)  # You can adjust the length as needed
    description = db.Column(db.Text, nullable=True)   # Assuming description can be nullable
    creator_id = db.Column(db.String(255), nullable=False)  # Adjust length as needed
    project_id = db.Column(db.Integer, nullable=False)
    pledge_amt = db.Column(db.Integer, nullable=False)
    price_id = db.Column(db.String(255), nullable=False)



    def __init__(self, option_id, title, description, creator_id, project_id, pledge_amt, price_id):
        self.option_id = option_id
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.project_id = project_id
        self.pledge_amt = pledge_amt
        self.price_id = price_id



    def json(self):
        return {"option_id": self.option_id,
                "title": self.title,
                "description": self.description,
                "creator_id": self.creator_id,
                "project_id": self.project_id,
                "pledge_amt": self.pledge_amt,
                "price_id": self.price_id,



@app.route("/options/<int:project_id>")
def get_option_by_project_id():
    optionlist = db.session.scalars(db.select(Pledge_option).filter_by(project_id=project_id))

    if len(optionlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "options": [option.json() for option in optionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no pledge options available."
        }
    ), 404




# @app.route("/project/<int:project_id>")
# def find_by_projectid(project_id):
#     project = db.session.scalars(
#         db.select(Project).filter_by(project_id=project_id).
#         limit(1)
# ).first()




#     if project:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": project.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Project not found."
#         }
#     ), 404

# find projects by creator_id
@app.route("/project/<creator_id>")
def find_by_creatorid(creator_id):
    # projectlist = db.session.scalars(db.select(Project)).all()

    projectlist = db.session.scalars(
        db.select(Project).filter_by(creator_id=creator_id)
    )

    if projectlist:
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
            "message": "No projects."
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
