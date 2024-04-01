FROM python:3-slim
# ENV STRIPE_API_URL=https://api.stripe.com/v1
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./tracker.py ./tracker.py
COPY ./amqp_connection.py ./amqp_connection.py
COPY ./amqp_setup.py ./amqp_setup.py
COPY ./utils.py ./utils.py
CMD [ "python", "tracker.py" ]