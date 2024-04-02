# ESD-Project-T3

# Crowdfunding

# Description
Creator needs funding for a Project and posts them on our Crowdfunding website. Anyone can visit the Crowdfunding website to explore Projects that interest them. They can become Backers if they decide to pledge for a Project. Backers are only charged at the end should the target amount is met, otherwise they will not be charged and the Project is cancelled. 

# How to set up application
Import project.sql found in Project folder
Import tracker.sql found in Tracker folder
Import activity_log.sql found in Activity_Log folder
Import error.sql found in Error folder
Import feedback.sql found in Feedback folder
Import user.sql found in User folder
Import pledge_options.sql found in Pledge_Options folder

# How to run application
- General
    Start MAMP/WAMP
    Open docker 
    Docker compose build
    Docker compose up 

- Frontend
    Backer: Bob
        Username: bob@gmail.com
        Password: bob
        user_id: 1

    Creator: Jack
        Username: jack@gmail.com
        Password: jack
        user_id: 2

# Grafana
    1. Go http://localhost:8002/ for Kong Manager
    2. Add a service 
        a. Name: trackerapi
        b. URL: http://tracker:5001/
    3. Add a route to trackerapi service
        a. Name: CREATE
        b. Method: POST
        c. Path: ~/project/\d{4}/tracker
        d. View 6 advanced fields > uncheck strip path
    4. Install the following Python module using pip:
        a. python -m pip install prometheus_flask_exporter
    5. Rebuild the tracker docker images and run the container again
    6. Run docker ps to get the Prometheus container ID
    7. Copy out the Prometheus’ configuration file to your local folder
        a. docker cp <prometheus_container_id>:/etc/prometheus/prometheus.yml ./
    8. Open a terminal at the location of the configuration file. Copy tracker.json and the updated file back to the Prometheus container
        a. docker cp tracker.json <prometheus_container_id>:/etc/prometheus/
    9. Copy out the Prometheus’ configuration file to your local folder
        a. docker cp prometheus.yml <prometheus_container_id>:/etc/prometheus/
    10. Login to Grafana at http://localhost:13000
        a. Default credentials admin / admin
        b. Change password to adminadmin
    11. Go to https://grafana.com/grafana/dashboards  and search for “flask”.
    12. You will find a dashboard called “flask transaction” whose ID is 9688 at time of update of this lab.
    13. Copy ID to clipboard
    14. Go back to your Grafana page http://localhost:13000/ >  > Dashboards
    15. Click the dropdown on the right > Import
    16. Paste the ID copied from Grafana website and click “Load”
    17. Click “Import”.
    18. Use Postman to send queries to your Kong API Gateway to generate some tracker services’ metrics for Prometheus to collect
        a. POST: http://127.0.0.1:5001/project/<project_id>/tracker
        b. Body: 
            {
                "user_id": 1,
                "pledge_amt": 5,
                "payment_intent_id": "pi_3OzlKoBWraf69XnW1G8GM5bl"
            }
    19. Open up the imported “flask transaction” dashboard

# Kong
    Endpoints Exposed in Kong
        1. projectapi http://project:5000/project
        plugins:
        - key_auth  (Ensure config.key_names has value “apikey”.)

        routes:
        - read_project /api/v1/project [GET]
        E.g. http://localhost:8000/api/v1/project?apikey=admin

        - read_specific_project ~/\d{4}  [GET] 
        - need to uncheck the strip option
        E.g. http://localhost:8000/1236?apikey=admin

        - read_creators_project ~/user_id=\d{1} [GET] 
        - need to uncheck the strip option
        E.g. http://localhost:8000/user_id=1?apikey=admin

        - create_project /api/v1/project [POST, OPTIONS] 
        - need to set up plugins: acl, cors in route
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/api/v1/project?apikey=admin

        2. trackerapi http://tracker:5001
        plugins:
        - key_auth (Ensure config.key_names has value “apikey”.)

        routes:
        - read_tracker ~/project/\d{4}/tracker [GET] 
        - need to uncheck the strip option
        E.g. http://localhost:8000/project/1236/tracker?apikey=admin

        - read_tracker_by_user ~/get_project_by_user_id/\d{1} [GET] 
        - need to uncheck the strip option
        E.g. http://localhost:8000/get_project_by_user_id/1?apikey=admin

        - create_tracker ~/project/\d{4}/tracker [POST, OPTIONS] 
        - need to uncheck the strip option and set up plugins: acl, cors in route
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/project/1236/tracker?apikey=admin

        - delete_tracker ~/tracker/\d{1} [DELETE] 
        - need to uncheck the strip option
        E.g. http://localhost:8000/tracker/1?apikey=admin

        3. backprojectapi http://back_project:5004
        plugins:
        - key_auth (Ensure config.key_names has value “apikey”.)

        routes:
        - create_checkout_session /create_checkout_session [POST, OPTIONS]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/create_checkout_session?apikey=admin

        - get_payment_intent_id ~/get_payment_intent_id/\.* [GET]
        - need to uncheck the strip option
        E.g. http://localhost:8000/get_payment_intent_id/cs_test_a1nxg5TKgeCrhmbFhPsPv?apikey=admin

        4. moderationapi http://moderation:5006
        plugins:
        - key_auth (Ensure config.key_names has value “apikey”.)

        routes:
        - moderate /moderate [POST, OPTIONS]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/moderate?apikey=admin

        5. feedbackapi http://feedback:5007
        plugins:
        - key_auth (Ensure config.key_names has value “apikey”.)

        routes:
        - get_feedback ~/get_feedback/\d{4}/ [GET]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/get_feedback/1236/?apikey=admin

        - create_feedback ~/create_feedback/\d{4}/ [POST, OPTIONS]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/create_feedback/1236/?apikey=admin

        6. pledgeoptionsapi http://pledge_options:5009
        plugins:
        - key_auth (Ensure config.key_names has value “apikey”.)
        
        routes:
        - get_options_by_project_id ~/options/\d{4} [GET]
        - need to uncheck the strip option and set up plugins: acl, cors
        E.g. http://localhost:8000/options/1236?apikey=admin

        - add_pledge_option ~/options/\d{4}/add [POST, OPTIONS]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/options/1236/add?apikey=admin

        - remove_option ~/options/\./*/remove [POST, OPTIONS]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/options/price_1OzXtuBWraf69XnWOJIEupXh/remove?apikey=admin

        7. userapi http://user:5010
        plugins:
        - key-auth (Ensure config.key_names has value “apikey”.)

        routes:
        - authenticate ~/user/auth [POST, OPTIONS]
        - need to uncheck the strip option and set up plugins: acl, cors
        - For ACL Section “config.allow” > Click “+ Add” > Enter “admins”
        E.g. http://localhost:8000/user/auth?apikey=admin

        - find_by_projectid ~/user/\d{1} [GET]
        - need to uncheck the strip option
        E.g. http://localhost:8000/user/1?apikey=admin