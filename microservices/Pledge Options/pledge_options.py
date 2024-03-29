from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS


from datetime import datetime

import requests
import sys
import pika
import json
import amqp_connection


exchangename = "pledge_options_topic" # exchange name
exchangetype = "topic" # use a 'direct' exchange to enable interaction


# #create a connection and a channel to the broker to publish messages to activity_log, error queues
# connection = amqp_connection.create_connection()
# channel = connection.channel()


# #if the exchange is not yet created, exit the program
# if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
#     print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
#     sys.exit(0)  # Exit with a success status


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/pledge_options'
# idk why it doesnt work if I use the above --> need to use command prompt for the above to work 
# use: set dbURL=mysql+mysqlconnector://root@localhost:3306/project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
headers = { "Authorization": "Bearer sk_test_51O4n0jBWraf69XnWY4aVlVKRqQUCAFfd39aPqRYrDH1tVCUDkUv73npLZXUJcMEopBma6kK2JdyZEdh8aRCij6Lk00clrvlXD8" }


db = SQLAlchemy(app)
CORS(app)  

class Pledge(db.Model):
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
        }


@app.route("/options/<int:project_id>")
def get_options_by_project_id(project_id):
    optionlist = db.session.scalars(db.select(Pledge).filter_by(project_id=project_id))

    if optionlist:
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


@app.route("/options/<int:project_id>/add", methods=['POST'])
def add_pledge_option(project_id):
    # return f"pledge option added to project {project_id}"
    data = request.get_json()
    # get all the data needed to create new price obj on stripe
    # product_id=data.get('product_id')
    product_id=data.get('product_id')
    pledge_amt=data.get('pledge_amt')
    
    params = {
        "product": product_id,
        "currency": "sgd",
        "unit_amount": pledge_amt * 100
    }
    stripe_url = "https://api.stripe.com/v1/prices"
    # send req to Stripe api to create a price obj for the product (project)
    try:
        response = requests.post(stripe_url, params=params, headers=headers).json()
    except Exception as e:
        error_message = {
            "error_type": "create_price_obj_error",
            "error_message": str(e),
            "data": data
        }
        # print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        # channel.basic_publish(exchange=exchangename, routing_key="project.error",
        #     body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
        # print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Price object in Stripe."
            }
        ), 500

    option = Pledge(
        creator_id=data.get('creator_id'),
        option_id=data.get('option_id'),
        title=data.get('title'),
        description=data.get('description'),
        project_id=data.get('project_id'),
        pledge_amt=data.get('pledge_amt'),
        price_id=response['id'],
    )
    # commit to database
    try:
        db.session.add(option)
        db.session.commit()
    except Exception as e:
        error_message = {
            "error_type": "create_option_error",
            "error_message": str(e),
            "data": data
        }
        # print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
        # channel.basic_publish(exchange=exchangename, routing_key="project.error",
        #     body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
        # print("\nProject error published to RabbitMQ Exchange.\n")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the pledge option."
            }
        ), 500


    return jsonify(
            {
                "code": 200,
                "data": response
            }
        )



    # project = Project(project_id = data.get('project_id'), name = data.get('name'), description = data.get('description'), creator_id = data.get('creator_id'), funding_goal = data.get('funding_goal'), deadline = data.get('deadline'), creation_time = data.get('creation_time'), status = data.get('status'), goal_reached = data.get('goal_reached'))


    # try:
    #     db.session.add(project)
    #     db.session.commit()
    # except Exception as e:
    #     error_message = {
    #         "error_type": "create_project_error",
    #         "error_message": str(e),
    #         "data": data
    #     }
    #     print('\n\n-----Publishing the (project error) message with routing_key=project.error-----')
    #     channel.basic_publish(exchange=exchangename, routing_key="project.error",
    #         body=json.dumps(error_message), properties=pika.BasicProperties(delivery_mode = 2))
    #     print("\nProject error published to RabbitMQ Exchange.\n")
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "message": "An error occurred creating the project."
    #         }
    #     ), 500
   
    # print('\n\n-----Publishing the (project info) message with routing_key=project.info-----')
    # channel.basic_publish(exchange=exchangename, routing_key="project.info",
    #     body=json.dumps(data), properties=pika.BasicProperties(delivery_mode = 2))
    # print("\nProject info published to RabbitMQ Exchange.\n")
    return jsonify(
        {
            "code": 201,
            "data": project.json()
        }
    ), 201


# @app.route("/project/<int:project_id>", methods=['PUT'])
# def update_project(project_id):
#     project = db.session.scalars(db.select(Project).filter_by(project_id=project_id).limit(1)).first()
#     if project:
#         data = request.get_json()
#         if data['goal_reached']:
#             project.goal_reached = data['goal_reached']
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": project.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "project_id": project_id
#             },
#             "message": "Project not found."
#         }
#     ), 404




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
