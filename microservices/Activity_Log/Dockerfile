FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./activity_log.py ./activity_log.py
COPY ./amqp_connection.py ./amqp_connection.py
CMD [ "python", "activity_log.py" ]