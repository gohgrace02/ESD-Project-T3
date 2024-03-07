from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# idk why it doesnt work if I use the above --> need to use command prompt for the above to work 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/project' --> hardcoding 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = 'project'



    projectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)  # You can adjust the length as needed
    description = db.Column(db.Text, nullable=True)   # Assuming description can be nullable
    creatorID = db.Column(db.String(255), nullable=False)  # Adjust length as needed
    fundingGoal = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    creationTime = db.Column(db.TIMESTAMP, nullable=False)
    Status = db.Column(db.String(255), nullable=False)  
    goalReached = db.Column(db.Boolean, nullable=False, default=False) # Default to False, as boolean.


    def __init__(self, projectID, name, description, creatorID, fundingGoal, deadline, creationTime, Status, goalReached):
        self.projectID = projectID
        self.name = name
        self.description = description
        self.creatorID = creatorID
        self.fundingGoal = fundingGoal
        self.deadline = deadline
        self.creationTime = creationTime
        self.Status = Status
        self.goalReached = goalReached


    def json(self):
        return {"projectID": self.projectID, "name": self.name, "description": self.description, "creatorID": self.creatorID, "fundingGoal": self.fundingGoal, "deadline": self.deadline, "creationTime": self.creationTime, "Status": self.Status, "goalReached": self.goalReached}

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


@app.route("/project/<string:projectID>")
def find_by_projectid(projectID):
    project = db.session.scalars(
    	db.select(Project).filter_by(projectID=projectID).
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


@app.route("/project/<string:projectID>", methods=['POST'])
def create_project(projectID):
    if (db.session.scalars(
      db.select(Project).filter_by(projectID=projectID).
      limit(1)
      ).first()
      ):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "projectID": projectID
                },
                "message": "Project already exists."
            }
        ), 400


    data = request.get_json()
    project = Project(projectID, **data)


    try:
        db.session.add(project)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "projectID": projectID
                },
                "message": "An error occurred creating the project."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": project.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)