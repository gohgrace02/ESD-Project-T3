from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import environ
from flask_cors import CORS

import os, sys



import requests

import pika
import json
# import amqp_connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
headers = { "Authorization": "Bearer sk_test_51O4n0jBWraf69XnWY4aVlVKRqQUCAFfd39aPqRYrDH1tVCUDkUv73npLZXUJcMEopBma6kK2JdyZEdh8aRCij6Lk00clrvlXD8" }


# back_project_URL = "http://localhost:5004/back_project"
# back_project_URL = "http://back_project:5004/back_project"
exchangename = "user" # exchange name
exchangetype = "direct" # use a 'direct' exchange to enable interaction

#create a connection and a channel to the broker to publish messages to activity_log, error queues
# connection = amqp_connection.create_connection() 
# channel = connection.channel()

# #if the exchange is not yet created, exit the program
# if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
#     print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
#     sys.exit(0)  # Exit with a success status

db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_creator = db.Column(db.Boolean, nullable=False)
    customer_id = db.Column(db.String(255))

    def __init__(self, user_id, name, email, password, is_creator, customer_id):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.is_creator = is_creator
        self.customer_id = customer_id

    def json(self):
        return {"user_id": self.user_id, 
                "name": self.name, 
                "email": self.email, 
                "password": self.password,
                "is_creator": self.is_creator,
                "customer_id": self.customer_id
        }
    


# get all users
@app.route("/user")
def get_all():
    userlist = db.session.scalars(db.select(User)).all()

    if len(userlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404


# get user by user_id
@app.route("/user/<int:user_id>")
def find_by_projectid(user_id):
    user = db.session.scalars(
        db.select(User).filter_by(user_id=user_id).
        limit(1)
).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404


# get user by email
@app.route("/user/auth", methods = ['POST'])
def authenticate():
    data = request.get_json()
    email = data.get('email')
    password_input = data.get('password')
    user = db.session.scalars(
        db.select(User).filter_by(email=email).
        limit(1)
).first()
    if user:
        # check if password input matches password in database
        database_password = user.password
        if password_input == database_password:
            return jsonify({
                "code": 201,
                "message": "User authenticated",
                "data": user.json()
            })
        else:
            return jsonify({
                "code": 401,
                "message": "Incorrect password"
            })
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)