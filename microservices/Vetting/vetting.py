from flask import Flask, request, jsonify
from requests import post
# from invokes import invoke_http
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

PROJECT_MICROSERVICE_URL = "http://localhost:5000/project"

def vet_project(project_data):
    # Add your vetting criteria here
    if 'name' in project_data and project_data['name'] == "ProjectNoNo": #checking works
        return False

    return True

@app.route("/vetting", methods=['POST'])
def vetting_endpoint():
    data = request.get_json()
    print("Data received:", data)
    
    if vet_project(data):
        # If vetting is approved, post the project to the project microservice
        response = post(PROJECT_MICROSERVICE_URL, json=data)

        if response.status_code == 201:
            return jsonify({"message": "Vetting successful. Project created."}), 200
        else:
            return jsonify(response.json()), response.status_code
        # print('project_result:', project_result)
        # project_result = invoke_http(PROJECT_MICROSERVICE_URL, method='POST', json=data)
        # return jsonify({"project_result:": project_result}), 200
    else:
        return jsonify({"message": "Project is not acceptable."}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)
if __name__ == "__main__":
  app.run(debug=True)