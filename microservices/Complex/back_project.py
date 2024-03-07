from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
import json

import os, sys

import requests

app = Flask(__name__)
CORS(app)

project_URL = "http://localhost:5000/project"
tracker_URL = "http://localhost:5001/project"
activity_log_URL = "http://localhost:5002/activity_log"
error_URL = "http://localhost:5003/error"
# stripe_URL = ""


# this is to display the UI which shows the available projects
@app.route("/back_project")
def list_projects():
    response = requests.get(project_URL).json()
    projects = response['data']['projects']
    return render_template('list_projects.html', projects=projects)

@app.route("/back_project/<string:projectID>")
def project_details(projectID):
    json_data_str = request.args.get('json_data')
    data = json.loads(json_data_str)
    return render_template('back_project.html', data=data)

# @app.route("/back_project/<string:projectID>")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

