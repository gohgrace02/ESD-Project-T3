from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests

app = Flask(__name__)
CORS(app)

project_URL = "http://localhost:5000/project"
tracker_URL = "http://localhost:5001/project"
activity_log_URL = "http://localhost:5002/activity_log"
error_URL = "http://localhost:5003/error"