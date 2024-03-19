FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./back_project.py ./back_project.py
COPY ./amqp_connection.py ./amqp_connection.py
CMD [ "python", "back_project.py" ]