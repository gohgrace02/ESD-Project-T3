FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./mod.py ./mod.py
COPY ./amqp_connection.py ./amqp_connection.py
COPY ./amqp_setup.py ./amqp_setup.py
CMD [ "python", "mod.py" ]